# API_SETUP_GUIDE.md

This guide provides step-by-step instructions on how to obtain and configure the necessary API keys for the "TSRS Moulsari AI Disaster Preparedness Evaluator." This project is designed to use free-tier APIs to minimize costs.

## Summary of Required APIs

1.  **Groq API**: For fast AI model inference (evaluation, feedback generation).
2.  **Hugging Face API**: For accessing embedding models and potentially other open-source models.
3.  **Google Gemini API (Optional)**: As a fallback or for specific tasks if Groq is unavailable.

---

## Environment Variable Setup

All API keys should be stored in a file named `.env` in the root directory of the project. This file is ignored by version control to keep your keys secure.

1.  **Create the `.env` file:**
    In the project's root folder, create a new file named `.env`.

2.  **Add the following lines** to the `.env` file, and then follow the guides below to get the actual key values:

    ```env
    # .env file

    # Groq API Key for fast LLM inference
    GROQ_API_KEY="YOUR_GROQ_API_KEY"

    # Hugging Face User Access Token for models/embeddings
    HUGGINGFACE_API_TOKEN="YOUR_HUGGINGFACE_API_TOKEN"

    # Google Gemini API Key (Optional Fallback)
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    ```

---

### 1. Groq API Key (Free Tier)

Groq provides the fastest available inference for several open-source language models. Their free tier is very generous and perfect for this project.

*   **Purpose**: Core AI evaluation and response generation.
*   **Website**: [GroqCloud](https://console.groq.com/keys)

**Steps to get your key:**

1.  **Navigate to the GroqCloud Console:**
    Go to the API Keys page: [https://console.groq.com/keys](https://console.groq.com/keys)

2.  **Sign In / Sign Up:**
    You will be prompted to log in. You can sign up for free using your Google or GitHub account.

3.  **Create a New API Key:**
    -   Once logged in, click the **"+ Create API Key"** button.
    -   Give the key a descriptive name, for example, `TSRS-AI-Evaluator`.
    -   Click "Create".

4.  **Copy Your Key:**
    -   Your new API key will be displayed. **This is the only time you will see the full key.**
    -   Click the copy icon to copy it to your clipboard.

5.  **Add to `.env` file:**
    -   Paste the key into your `.env` file as the value for `GROQ_API_KEY`.

    ```env
    GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```

---

### 2. Hugging Face API Token

A Hugging Face token is needed to download and use certain models and embeddings from the Hugging Face Hub without rate limits.

*   **Purpose**: Accessing sentence-transformer models for embeddings.
*   **Website**: [Hugging Face Settings](https://huggingface.co/settings/tokens)

**Steps to get your token:**

1.  **Navigate to your Hugging Face Access Tokens page:**
    Go to: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

2.  **Sign In / Sign Up:**
    Log in to your Hugging Face account or create a new one for free.

3.  **Create a New Token:**
    -   Click the **"New token"** button.
    -   Give the token a name, like `TSRS-AI-Evaluator`.
    -   Assign it a `read` role, as we only need to download models.
    -   Click **"Generate a token"**.

4.  **Copy Your Token:**
    -   Your new token will be displayed. Click the copy icon next to it.

5.  **Add to `.env` file:**
    -   Paste the token into your `.env` file as the value for `HUGGINGFACE_API_TOKEN`.

    ```env
    HUGGINGFACE_API_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```

---

### 3. Google Gemini API Key (Optional)

This is an optional but recommended fallback. Google's Gemini Pro model is available via a free tier that is suitable for this project's scale.

*   **Purpose**: Fallback for AI evaluation if Groq is down.
*   **Website**: [Google AI Studio](https://aistudio.google.com/app/apikey)

**Steps to get your key:**

1.  **Navigate to Google AI Studio:**
    Go to: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

2.  **Sign In:**
    Log in with your Google account.

3.  **Create a New API Key:**
    -   You may need to agree to the terms of service first.
    -   Click the **"Create API key in new project"** button.

4.  **Copy Your Key:**
    -   A new API key will be generated and displayed in a pop-up.
    -   Copy the key.

5.  **Add to `.env` file:**
    -   Paste the key into your `.env` file as the value for `GOOGLE_API_KEY`.

    ```env
    GOOGLE_API_KEY="AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```

---

## Final Check

Your `.env` file should now look something like this, but with your actual keys:

```env
# .env file

# Groq API Key for fast LLM inference
GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Hugging Face User Access Token for models/embeddings
HUGGINGFACE_API_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Google Gemini API Key (Optional Fallback)
GOOGLE_API_KEY="AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

With this file in place, the application will automatically load these keys when it starts. **Do not share this file or commit it to version control.**
