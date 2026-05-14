# TSRS Moulsari AI Disaster Preparedness Evaluator

This AI-powered system evaluates how prepared students are to respond during emergencies and disaster situations at The Shri Ram School Moulsari. The interview simulates realistic scenarios such as earthquakes, fires, cybersecurity incidents, lockdowns, and emergency evacuations. Based on your responses, the AI estimates your preparedness level and provides personalized feedback.

## Getting Started

Follow these steps to set up and run the project on your local machine.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd AI_Interviewer
```

### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

**On Windows:**

```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

**On macOS and Linux:**

```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

The application requires API keys for Groq and Hugging Face.

1.  Make a copy of the example environment file.
    *   On Windows: `copy .env.example .env`
    *   On macOS/Linux: `cp .env.example .env`
2.  Open the newly created `.env` file.
3.  Follow the instructions in [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) to get your free API keys.
4.  Paste your keys into the `.env` file.

### 5. Prepare Your Data

Place your school's specific emergency protocol documents (PDF, TXT, etc.) into the `/data` directory. For more details, see the [DATA_SETUP_GUIDE.md](DATA_SETUP_GUIDE.md).

### 6. Run the RAG Ingestion Pipeline

This step processes your documents and builds the knowledge base for the AI.

```bash
python -m rag.ingest
```

### 7. Run the Streamlit Application

You are now ready to start the web application!

```bash
streamlit run app.py
```

The application should open in your web browser automatically.

