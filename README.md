Esta solución utiliza varias tecnologías y bibliotecas clave para ofrecer un asistente educativo interactivo basado en procesamiento de lenguaje natural y almacenamiento de documentos. A continuación, te desgloso las tecnologías utilizadas:

## 1. Lenguaje de Programación
Python: El código está escrito en Python, un lenguaje ampliamente utilizado en el campo de la inteligencia artificial, procesamiento de lenguaje natural (NLP) y desarrollo web.

## 2. Librerías de Inteligencia Artificial y NLP
- LangChain: Utilizada para crear flujos de trabajo complejos con modelos de lenguaje, integrando:
- Document Loaders: Para cargar documentos desde distintos formatos (PDF, TXT).
- Text Splitters: Para dividir textos largos en partes más pequeñas y manejables.
- Embeddings: Para convertir texto en vectores de alta dimensión.
- ConversationalRetrievalChain: Para construir un sistema de preguntas y respuestas con memoria.
- Memory: Para guardar el historial de la conversación, permitiendo una interacción más fluida.
- OpenAI: A través de la API de OpenAI, se utilizan los modelos GPT (en este caso, gpt-3.5-turbo) para generar respuestas a preguntas basadas en los documentos cargados.
- Chroma: Se utiliza para la gestión de vectores y búsqueda semántica. Chroma es una base de datos de vectores persistente que permite realizar consultas eficientes sobre grandes volúmenes de datos textuales.

## 3. Almacenamiento y Base de Datos
- ChromaDB: Se usa para almacenar y realizar búsquedas sobre documentos cargados. La base de datos está configurada para persistir los vectores de texto generados por los embeddings y almacenarlos localmente.
- PersistentClient: Permite que la base de datos sea persistente, guardando los datos entre reinicios de la aplicación.

## 4. Frameworks de Desarrollo
- Streamlit: Un framework para crear interfaces web de manera sencilla y rápida. Aquí se utiliza para construir la interfaz de usuario (UI), mostrando los mensajes del chat y permitiendo la carga de documentos y la interacción con el asistente.

## 5. Tecnologías de Interacción y Desarrollo Web
- HTML y CSS (a través de Streamlit): Streamlit genera la UI automáticamente, pero bajo el capó, utiliza HTML y CSS para crear las interfaces de usuario.
- Python File Handling: Para manejar la carga de archivos temporales (PDF o TXT) y pasarlos al sistema para su procesamiento.

## Flujo del Sistema
- El usuario sube documentos (PDF o TXT) a través de Streamlit.
- Los documentos son cargados y procesados usando PyPDFLoader o TextLoader.
- Los textos se dividen en fragmentos manejables usando RecursiveCharacterTextSplitter.
- Los fragmentos de texto se convierten en vectores utilizando OpenAIEmbeddings y se almacenan en ChromaDB.
- El sistema responde a preguntas utilizando ChatOpenAI con ConversationalRetrievalChain para buscar respuestas relevantes en los documentos.
- El historial de la conversación se mantiene con ConversationBufferMemory, permitiendo un flujo continuo de interacción.

### Conclusión
Esta solución integra varias tecnologías de inteligencia artificial y desarrollo web para ofrecer una experiencia interactiva basada en texto, permitiendo al usuario cargar documentos y hacer preguntas basadas en ellos. Las tecnologías clave son LangChain, Streamlit, ChromaDB y OpenAI.

## Resumen de las Tecnologías Usadas:

- Python: Lenguaje de programación utilizado para el desarrollo de la aplicación.
- LangChain: Biblioteca para trabajar con modelos de lenguaje y gestionar interacciones de preguntas y respuestas.
- OpenAI API: Proveedor de modelos de lenguaje (GPT-3.5) para generar respuestas.
- ChromaDB: Base de datos vectorial persistente utilizada para almacenar y recuperar los vectores de texto.
- Streamlit: Framework para crear la interfaz de usuario interactiva para el chat.
- PyPDFLoader / TextLoader: Cargadores de documentos para procesar archivos PDF y TXT.
- RecursiveCharacterTextSplitter: Técnica para dividir los textos largos en fragmentos más pequeños.
- ConversationBufferMemory: Memoria para almacenar el historial de la conversación y permitir interacciones continuas.

## Para levantar el proyecto:
Situarse en el directorio principal
```bash
python -m venv env    
env\Scripts\activate  
pip install -r requirements.txt
streamlit run petroia.py