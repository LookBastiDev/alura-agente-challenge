import os
import requests
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ==========================================
# CONFIGURACIÓN Y CLIENTE COHERE
# ==========================================

load_dotenv()

def obtener_modelo_cohere(api_key):
    print("🔍 Consultando a Cohere los modelos disponibles...")
    url = "https://api.cohere.com/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            modelos = resp.json().get('models', [])
            modelos_chat = [m['name'] for m in modelos if 'endpoints' in m and 'chat' in m['endpoints']]
            
            if not modelos_chat:
                return "command-r-plus"
                
            print(f"📋 Cohere tiene {len(modelos_chat)} modelos de chat disponibles.")
            for m in modelos_chat:
                if 'plus' in m or '05-2026' in m:
                    print(f"✔️ Modelo seleccionado: {m}")
                    return m
                    
            return modelos_chat[0]
        else:
            return "command-r-plus"
    except Exception:
        return "command-r-plus"

def consultar_cohere_directo(contexto, pregunta, api_key, modelo_nombre):
    url = "https://api.cohere.com/v2/chat"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    
    prompt = (
        "Eres un asistente corporativo experto. Usa los siguientes fragmentos de contexto "
        "recuperado del documento interno para responder a la pregunta del usuario. "
        "Si la respuesta no está en el documento, di amablemente que no tienes esa información.\n\n"
        f"Contexto del documento:\n{contexto}"
    )
    
    payload = {
        "model": modelo_nombre,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": pregunta}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            datos = response.json()
            try:
                for bloque in datos['message']['content']:
                    if bloque.get('type') == 'text':
                        return bloque['text']
                return str(datos)
            except Exception:
                return str(datos)
        else:
            return f"Error en la API de Cohere: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error de red: {e}"

# ==========================================
# LÓGICA PRINCIPAL DEL AGENTE
# ==========================================

def iniciar_agente():
    print("🤖 Iniciando el Agente IA con Cohere V2... Procesando documento...")
    
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        print("❌ Error: No se encontró COHERE_API_KEY en el archivo .env")
        return
        
    modelo_disponible = obtener_modelo_cohere(api_key)

    pdf_path = "documento.pdf"
    if not os.path.exists(pdf_path):
        print(f"❌ Error: No se encontró '{pdf_path}'. Pon tu PDF en esta carpeta.")
        return

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    print("⏳ Creando base de datos vectorial (memoria local)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(splits, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    print("\n✅ ¡Agente listo! Hazme una pregunta sobre el documento. (Escribe 'salir' para terminar)\n")

    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ['salir', 'exit', 'quit']:
            print("¡Hasta luego!")
            break
        
        documentos_recuperados = retriever.invoke(user_input)
        contexto = "\n\n".join([doc.page_content for doc in documentos_recuperados])
        
        respuesta = consultar_cohere_directo(contexto, user_input, api_key, modelo_disponible)
        print(f"\n🤖 Agente: {respuesta}\n")

if __name__ == "__main__":
    iniciar_agente()