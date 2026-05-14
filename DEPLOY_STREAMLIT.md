# Deploying to Streamlit Cloud (streamlit.io) via GitHub

This document explains step-by-step how to deploy this project to Streamlit Cloud using a GitHub repository. It also explains what will and will not transfer automatically (models, large files, and the vector DB), and provides recommendations.

IMPORTANT: Streamlit Cloud runs your code directly from your GitHub repo. Large model weights and local databases are typically too big to include in a repo — you may need to use hosted model APIs, cloud storage, or re-run ingestion on the cloud.

---

## 1) Prepare your repository

1. Create a GitHub repository and push the project to it (do not include your local virtualenv or large data files).

   Example commands:

```bash
git init
git add .
git commit -m "Initial commit: AI_Interviewer"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

2. Add a `.gitignore` that excludes `venv`, `.env`, and other large files. Example entries:

```
venv/
.env
__pycache__/
*.pyc
data/*
*.model
```

Note: If you have small data files you want included, keep them under a `data-small/` directory and commit them. For large datasets use cloud storage (S3, GCS) or Git LFS.

---

## 2) Make the app Streamlit-ready

1. Ensure `app.py` is at the repository root and is the Streamlit entrypoint. Streamlit Cloud will run `streamlit run app.py` by default.
2. Make sure `requirements.txt` lists all required packages. If your project uses specific system dependencies, note them in the README and consider using a Docker deployment (advanced).

Example minimal `requirements.txt` headers:

```
streamlit
sounddevice
faster-whisper
scipy
numpy
langchain
chromadb
huggingface-hub
```

3. Remove any hard-coded absolute paths; use relative paths and environment variables for secrets and API keys.

---

## 3) Secrets and environment variables on Streamlit Cloud

Streamlit Cloud provides a secrets manager where you can add environment variables, API keys, and other secrets.

1. In Streamlit Cloud, open your app settings → Secrets.
2. Add the entries from your local `.env` (do NOT commit `.env` to GitHub). For example:

```
GROQ_API_KEY = "xxxx"
HUGGINGFACE_API_KEY = "xxxx"
CHROMA_DB_PATH = "./chroma_store"
```

3. In your code, read these with `os.environ.get('GROQ_API_KEY')` or Streamlit's `st.secrets`.

---

## 4) Handling large model weights and local vector DBs

- Models (LLMs) and large local weights:
  - If you use a cloud API (Groq, OpenAI, Hugging Face Inference, etc.), the credentials and calls will work on Streamlit Cloud once secrets are set.
  - If you use local model files (weights), they will not be uploaded to GitHub (and should not). Options:
    - Host your own model on a separate server or inference API and call it from the app.
    - Use a hosted model provider (recommended).
    - If you must include model files, use Git LFS and be aware of storage/bandwidth limits.

- Vector DB (Chroma/FAISS):
  - If the local vector DB is created at runtime (via `rag.ingest`), the simplest option is to re-run ingestion on Streamlit Cloud during the first start (it may take time and consume RAM/CPU).
  - Alternatively, persist the vector DB files to cloud storage and restore them at startup.

Recommendation: For a straightforward deployment, rely on hosted LLM APIs and re-run the ingestion on the cloud (or use a small subset of data committed to the repo).

---

## 5) Link GitHub repo to Streamlit Cloud and deploy

1. Go to https://streamlit.io/cloud and sign in with GitHub.
2. Click "New app" → choose the GitHub repo and the branch to deploy (e.g., `main`).
3. For "File in repository", enter `app.py`.
4. Click "Deploy".

Streamlit Cloud will install dependencies from `requirements.txt`, build the app, and run it. Watch the logs for errors.

---

## 6) Post-deploy steps and validation

1. Open the deployed app URL provided by Streamlit Cloud.
2. Verify the UI and basic interactions.
3. If your app needs the vector DB, run the ingestion step remotely (via a button in the web UI or by running a one-off command on the machine where the app runs). If ingestion requires heavy CPU, consider doing it externally and uploading the resulting DB files.

---

## 7) Troubleshooting common issues

- Missing dependencies: Ensure all libraries are listed in `requirements.txt`.
- Secret not found errors: Make sure you added the secret to Streamlit Cloud and that code reads from `os.environ` or `st.secrets`.
- Large model memory errors: Use a hosted inference API instead of local weights.
- Audio device errors: Streamlit Cloud does not provide access to your local microphone — interactive mic recording won't work in the hosted server. For user audio input on the web, consider using the browser to capture audio and upload it from the client-side.

---

## 8) Summary: what transfers automatically vs not

- Transfers that happen automatically when you push to GitHub:
  - Source code (`.py`, `.md`, `.css`, frontend assets)
  - Small data files committed to the repo
  - `requirements.txt`

- Things that do NOT automatically transfer and need separate handling:
  - Local model weights and LLM checkpoints (use hosted APIs or Git LFS)
  - Local vector DB files (re-run ingestion on the cloud or restore from cloud storage)
  - Local OS-level resources like microphone access (client-side only)

---

If you want, I can:
- Add a small `deploy.sh` script or GitHub Actions workflow that triggers re-indexing and deploy steps.
- Add a short note in the README linking to this `DEPLOY_STREAMLIT.md`.
