import os
import chromadb
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
#from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from typing import List, Dict
import streamlit as st

class AsistenteEducativo:
    def __init__(self, api_key: str):
        """
        Inicializa el asistente virtual 
        
        Args:
            api_key (str): API key de OpenAI
        """
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Crear directorio para la base de datos si no existe
        self.persist_directory = "chroma_db"
        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)
            
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        self.llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
        self.db = None
        self.qa_chain = None

    def cargar_documentos(self, rutas_documentos: List[str]) -> None:
        """
        Carga y procesa los documentos fuente.
        
        Args:
            rutas_documentos (List[str]): Lista de rutas a los documentos
        """
        # Configurar cliente de Chroma
        chroma_client = chromadb.PersistentClient(path=self.persist_directory)
        
        documentos = []
        for ruta in rutas_documentos:
            if ruta.endswith('.pdf'):
                loader = PyPDFLoader(ruta)
            else:
                loader = TextLoader(ruta)
            documentos.extend(loader.load())

        textos = self.text_splitter.split_documents(documentos)
        
        # Crear base de datos vectorial con persistencia
        self.db = Chroma.from_documents(
            documents=textos,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            client=chroma_client
        )
        
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.db.as_retriever(),
            memory=self.memory,
            return_source_documents=True,
            verbose=True
        )

    def responder_pregunta(self, pregunta: str) -> Dict:
        """
        Responde a una pregunta basándose en los documentos cargados.
        
        Args:
            pregunta (str): Pregunta del usuario
            
        Returns:
            Dict: Diccionario con la respuesta y documentos fuente
        """
        if not self.qa_chain:
            raise ValueError("No se han cargado documentos aún.")
            
        resultado = self.qa_chain({"question": pregunta})
        return {
            "respuesta": resultado["answer"],
            "documentos_fuente": resultado["source_documents"]
        }

def main():
    st.title("MVP Asistente PetroIA a escalar")
    
    # Configuración inicial
    if 'asistente' not in st.session_state:
        api_key = st.text_input("Ingresa tu API key de OpenAI:", type="password")
        if api_key:
            st.session_state.asistente = AsistenteEducativo(api_key)
            st.success("¡Asistente inicializado correctamente!")

    # Carga de documentos
    if 'asistente' in st.session_state:
        uploaded_files = st.file_uploader(
            "Carga tus documentos (PDF o TXT)",
            accept_multiple_files=True,
            type=['pdf', 'txt']
        )
        
        if uploaded_files:
            rutas_temp = []
            for archivo in uploaded_files:
                ruta_temp = f"temp_{archivo.name}"
                with open(ruta_temp, "wb") as f:
                    f.write(archivo.getbuffer())
                rutas_temp.append(ruta_temp)
                
            try:
                st.session_state.asistente.cargar_documentos(rutas_temp)
                st.success("¡Documentos cargados exitosamente!")
            except Exception as e:
                st.error(f"Error al cargar documentos: {str(e)}")
            finally:
                # Limpiar archivos temporales
                for ruta in rutas_temp:
                    if os.path.exists(ruta):
                        os.remove(ruta)

        # Interface de chat
        if 'mensajes' not in st.session_state:
            st.session_state.mensajes = []

        # Mostrar historial de mensajes
        for mensaje in st.session_state.mensajes:
            with st.chat_message(mensaje["rol"]):
                st.write(mensaje["contenido"])

        # Campo de entrada para la pregunta
        pregunta = st.chat_input("Hazme una pregunta sobre los documentos:")
        if pregunta:
            # Mostrar la pregunta del usuario
            with st.chat_message("user"):
                st.write(pregunta)
            st.session_state.mensajes.append({"rol": "user", "contenido": pregunta})

            try:
                # Mostrar la respuesta del asistente
                with st.chat_message("assistant"):
                    respuesta = st.session_state.asistente.responder_pregunta(pregunta)
                    st.write(respuesta["respuesta"])
                    st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta["respuesta"]})
                    
                    with st.expander("Ver documentos fuente"):
                        for i, doc in enumerate(respuesta["documentos_fuente"]):
                            st.write(f"Documento {i+1}:")
                            st.write(doc.page_content)
            except ValueError as e:
                st.error(str(e))

if __name__ == "__main__":
    main()