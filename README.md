# TSRS Moulsari AI Disaster Preparedness Evaluator

TSRS Moulsari AI Disaster Preparedness Evaluator is an advanced scenario-intelligence platform designed to measure how effectively students can reason, prioritize, and act under pressure during both cybersecurity incidents and real-world natural disasters. The system runs a high-fidelity adaptive interview loop that continuously updates difficulty and question sequencing based on each response, creating a personalized assessment path instead of a static quiz. In cyber-focused tracks, the interviewer simulates phishing attempts, credential compromise events, unsafe link interactions, suspicious device behavior, and social engineering pressure tests to evaluate recognition speed, escalation decisions, and digital hygiene practices. In disaster-focused tracks, it models high-stress environments such as earthquake protocols, fire response, evacuation control, lockdown compliance, flood readiness, and communication under uncertainty, scoring students on procedural correctness, safety awareness, situational calmness, and decision clarity.

Under the hood, the platform uses a retrieval-augmented evaluation architecture with a domain-tuned interview engine, rubric-conditioned scoring prompts, and context-aware reasoning chains to simulate an institution-specific expert assessor. The question flow is dynamically composed from scenario templates, risk metadata, and prior answer signals, enabling targeted follow-ups when a response indicates confusion, misconception, or overconfidence. A speech-to-text pipeline converts spoken responses into analyzable text, after which the evaluator generates structured category scores, strengths, weaknesses, misconception flags, and guidance for corrective learning. The system then compiles all rounds into a comprehensive final preparedness report that highlights performance trends, identifies critical failure points, and recommends actionable improvement priorities for students, educators, and safety coordinators.

In practical terms, this project acts like a technical readiness copilot for school safety operations: it converts qualitative student behavior into measurable intelligence, produces explainable analytics, and supports data-driven preparedness programs spanning both cyber resilience and emergency response readiness.

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

