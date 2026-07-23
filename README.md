# 🤖 Alura Agente Challenge - Bastián Ignacio Cerda Báez

Este proyecto es un Agente de Inteligencia Artificial basado en la arquitectura **RAG (Retrieval-Augmented Generation)**, diseñado para leer documentos corporativos internos y responder preguntas en lenguaje natural sin necesidad de que el usuario busque manualmente en el texto.

## 🏗 Arquitectura
* **Lenguaje:** Python
* **Orquestador:** LangChain
* **Procesamiento de Documentos:** PyPDF
* **Base de Datos Vectorial:** FAISS (Facebook AI Similarity Search)
* **LLM & Embeddings:** Google Gemini (gemini-1.5-flash & embedding-001)

## 💬 Ejemplos de uso
**Usuario:** ¿Cuáles son las condiciones para solicitar un reembolso?
**Agente:** Según la política, los reembolsos solo se aplican a productos devueltos dentro de los primeros 30 días con su empaque original.

*(Nota: Agrega 2 preguntas y respuestas que te haya dado tu script al probarlo con tu documento específico)*

## 🚀 Cómo ejecutarlo localmente
1. Clona este repositorio.
2. Instala las dependencias: `pip install -r requirements.txt`
3. Crea un archivo `.env` en la raíz y agrega tu API Key: `GOOGLE_API_KEY=tu_clave_aqui`
4. Ejecuta el script: `python agente.py`

## ☁️ Deploy en Oracle Cloud Infrastructure (OCI)
![Deploy OCI](LINK_A_TU_CAPTURA_AQUI)
*El agente se encuentra desplegado y ejecutándose correctamente en una instancia de OCI Compute.*