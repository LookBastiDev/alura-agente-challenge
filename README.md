# 🤖 Alura Agente Challenge - Bastián Ignacio Cerda Báez

Este proyecto es un Agente de Inteligencia Artificial basado en la arquitectura **RAG (Retrieval-Augmented Generation)**, diseñado para procesar documentos corporativos internos y responder preguntas en lenguaje natural sin necesidad de que el colaborador lea el archivo completo.

## 🏗 Arquitectura y Tecnologías
* **Lenguaje:** Python
* **Orquestador RAG:** LangChain
* **Procesamiento de Documentos:** PyPDFLoader (división de texto con RecursiveCharacterTextSplitter)
* **Embeddings y Base de Datos Vectorial:** HuggingFace (`all-MiniLM-L6-v2`) con FAISS (búsqueda de similitud local)
* **LLM:** Cohere API V2 (Modelo `command-a-plus-05-2026` / `command-r-plus`) conectado vía peticiones REST directas.

## 💬 Ejemplos de Preguntas y Respuestas
**Usuario:** ¿Cuáles son las situaciones que requieren escalamiento según la política?
**Agente:** Según la sección 31 del documento, las situaciones que requieren escalamiento incluyen cobros sin orden visible, discrepancias entre evidencia y relato, y solicitudes de revisión de nivel superior.

**Usuario:** ¿Me puedes decir el contenido que tiene documento.pdf?
**Agente:** No tengo el archivo completo de documento.pdf. Lo que tengo es un extracto de una política interna que incluye notas de coordinación, matriz orientativa de decisión, preguntas frecuentes sobre devoluciones y criterios de escalamiento.

## 🚀 Instrucciones para ejecutar el proyecto localmente
1. Clona este repositorio en tu máquina local.
2. Crea un entorno virtual e instala las dependencias: 
   ```bash
   pip install -r requirements.txt