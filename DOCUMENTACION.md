# 📚 Documentación Técnica: Agente RAG en OCI

## 1. Arquitectura del Sistema

El proyecto fue diseñado utilizando una arquitectura RAG (Retrieval-Augmented Generation) desplegada íntegramente en la nube. A continuación se detalla el flujo de la información:

```mermaid
graph TD
    A[Usuario] -->|Consulta vía SSH| B(Servidor OCI - Ubuntu 22.04)
    B --> C{Orquestador LangChain}
    C -->|1. Ingesta de PDF| D[PyPDFLoader + Text Splitter]
    D -->|2. Creación de Embeddings| E[(FAISS Vector Store local)]
    E -->|3. Recupera Contextos (k=3)| C
    C -->|4. Construcción de Prompt| F[Cohere API V2 <br> Modelo: command-a-plus]
    F -->|5. Respuesta Generada| B
    B -->|Muestra tabla/texto| A
```

## 2. Tecnologías y Herramientas Utilizadas
* **Infraestructura (Cloud):** Oracle Cloud Infrastructure (OCI) Compute Instance.
* **Sistema Operativo:** Ubuntu 22.04 LTS.
* **Orquestación de IA:** LangChain Core & Community.
* **Base de Datos Vectorial:** FAISS (Facebook AI Similarity Search).
* **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`).
* **LLM:** Cohere API V2 con sistema de **autodescubrimiento de modelos en tiempo real** (Modelo detectado autónomamente: `command-a-plus-05-2026`).


## 3. Desafíos de Ingeniería Resueltos durante el Deploy

Durante la migración del entorno local (Windows) al entorno de producción (OCI Ubuntu), se resolvieron los siguientes bloqueos técnicos:

### A. Gestión de Memoria (OOM Killer)
* **Problema:** La instancia gratuita "Micro" de OCI (1GB RAM) colapsaba al intentar compilar las dependencias pesadas de Machine Learning (`torch`), activando el proceso *Killed* del sistema operativo.
* **Solución:** Se provisionaron 2GB de memoria virtual (SWAP) directamente en el disco duro mediante `fallocate` y se reconfiguró `pip` para instalar sin usar la caché (`--no-cache-dir`), optimizando el uso de RAM.

### B. Conflicto de Dependencias (NumPy vs FAISS)
* **Problema:** La resolución automática de dependencias instaló NumPy 2.x, el cual rompió la compatibilidad con los binarios precompilados de `faiss-cpu`.
* **Solución:** Se realizó un *downgrade* forzado a la versión 1.x de NumPy en el entorno virtual (`pip install "numpy<2"`), restaurando la comunicación con la base de datos vectorial.

### C. Evolución de la API del LLM
* **Problema:** Los modelos modernos de Cohere (2026) ya no son soportados por la API V1 (`/v1/chat`), provocando errores HTTP 400 y 422.
* **Solución:** Se reestructuró la función de conexión directa en el script `agente.py` para apuntar al endpoint `/v2/chat`, implementando la nueva estructura de arreglos JSON (`messages`, `role`, `content`) exigida por el proveedor.

### D. Autodescubrimiento Dinámico de Modelos (Radar de IA)
* **Problema:** Los proveedores de IA deprecian y eliminan modelos antiguos constantemente (ej. el error 404 por la eliminación del modelo `command` clásico). Un código con el nombre del modelo escrito "en duro" (hardcoded) tiene una vida útil corta.
* **Solución:** Se diseñó una función de autodescubrimiento que se conecta a la API de Cohere al inicializar el agente, consulta la lista completa de modelos vivos en tiempo real, filtra exclusivamente los que tienen endpoints de `chat`, y selecciona de forma autónoma el modelo más avanzado disponible en la cuenta del usuario (en este caso, detectó y asignó automáticamente `command-a-plus-05-2026`). Esto hace que el código sea escalable y a prueba de obsolescencia.

## 4. Evidencia de Ejecución en Producción

<img width="1292" height="870" alt="Screenshot 2026-07-22 223450" src="https://github.com/user-attachments/assets/aea5f907-8ed3-4395-9783-6ae4d11c5500" />

<img width="1258" height="846" alt="Screenshot 2026-07-22 223500" src="https://github.com/user-attachments/assets/ab9f8360-136f-402a-932a-3d5aef3ed143" />

<img width="1282" height="806" alt="Screenshot 2026-07-22 223513" src="https://github.com/user-attachments/assets/8f9de053-c313-4481-be2b-608e8a8b1643" />



