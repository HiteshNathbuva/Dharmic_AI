# Dharmic AI

Dharmic AI is a Retrieval-Augmented Generation (RAG) chatbot for answering questions about Dharmic scriptures and ethics. It is designed as a focused assistant that retrieves relevant scripture records and returns grounded, human-readable answers for Dharmic topics.

The project uses a Flask backend, FAISS vector search, SentenceTransformers embeddings, and a static HTML/CSS/JavaScript frontend.

## Features

- Answers questions related to Dharma, Karma, ethics, and scriptures.
- Rejects questions outside the Dharmic domain.
- Uses FAISS for semantic retrieval over scripture metadata.
- Uses `sentence-transformers/all-MiniLM-L6-v2` for embeddings.
- Returns structured responses with summary, explanation, verses, sources, confidence, and disclaimer.
- Provides a lightweight browser-based chat interface.
- Includes light and dark theme support in the frontend.

## Project Structure

```text
Dharmic_AI/
├── backend/
│   └── app.py
├── data/
│   ├── faiss.index
│   └── metadata_merged.json
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── scripts/
│   └── answer_generator.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.10 or newer is recommended.
- A modern web browser.
- Internet access for the first installation of Python packages and the embedding model.

## Installation

Clone the repository:

```bash
git clone https://github.com/HiteshNathbuva/Dharmic_AI.git
cd Dharmic_AI
```

## Virtual Environment Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

## Dependency Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Environment Variable Setup

Create a local `.env` file from the example file:

```bash
cp .env.example .env
```

On Windows PowerShell, use:

```powershell
Copy-Item .env.example .env
```

The current application does not require secrets to run locally. The `.env.example` file is provided as a safe template for future configuration.

## Run the Backend

From the repository root, start the Flask backend:

```bash
python backend/app.py
```

The backend runs on:

```text
http://127.0.0.1:5000/
```

Open that URL in a browser to confirm the backend is running. You should see a success message.

## Run the Frontend

Open the frontend file in a browser:

```text
frontend/index.html
```

The frontend sends chat requests to:

```text
http://127.0.0.1:5000/ask
```

Keep the backend running while using the chat interface.

## How It Works

1. The user enters a question in the frontend.
2. The frontend sends the question to the Flask `/ask` endpoint.
3. The backend checks intent, domain relevance, and safety rules.
4. The question is embedded with SentenceTransformers.
5. FAISS retrieves relevant scripture records from the local index.
6. The answer generator builds a structured Dharmic response.
7. The frontend renders the response in the chat UI.

## Troubleshooting

If the browser shows "site cannot be reached", make sure the Flask backend is running.

If Python cannot find the data files, run the backend from the repository root:

```bash
python backend/app.py
```

If package installation fails for FAISS, confirm that you are using a supported Python version and reinstall dependencies inside a clean virtual environment.

## Security Note

Do not commit real `.env` files or secrets. Use `.env.example` only for placeholder configuration.
