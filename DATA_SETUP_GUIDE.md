# DATA_SETUP_GUIDE.md

This guide explains how to customize the "TSRS Moulsari AI Disaster Preparedness Evaluator" with your school's specific documents, questions, and evaluation criteria.

## Overview of Customization

The power of this system comes from its Retrieval-Augmented Generation (RAG) pipeline. By providing it with your school's actual disaster preparedness documents, the AI can give much more relevant and accurate evaluations.

You can customize:
1.  **The Knowledge Base**: Add PDFs, text files, and images containing your school's emergency protocols.
2.  **The Interview Questions**: Modify existing questions or add new ones to reflect specific concerns.

---

## 1. How to Add School-Specific Documents (The Knowledge Base)

The RAG system ingests documents from the `/data` directory. This is where you should place all relevant files.

**Supported File Types:**
*   `.pdf`: Scanned documents, official protocols.
*   `.txt`: Plain text notes, simple instructions.
*   `.md`: Markdown files, formatted documents.
*   `.png`, `.jpg`, `.jpeg`: Images containing text, such as maps with legends, scanned notices, or infographics. The system will automatically perform Optical Character Recognition (OCR) to extract text from these images.

### Steps to Add Documents:

1.  **Gather Your Documents:**
    Collect all relevant materials. Examples include:
    *   Evacuation route maps (`evacuation_routes.pdf`, `campus_map.jpg`)
    *   Fire safety procedures (`fire_safety_protocol.pdf`)
    *   Earthquake "drop, cover, and hold on" instructions (`earthquake_drill.txt`)
    *   Lockdown procedures (`lockdown_rules.md`)
    *   Cybersecurity best practices for students (`cyber_rules.pdf`)
    *   Emergency contact lists (`emergency_contacts.txt`)

2.  **Place Files in the `/data` Directory:**
    -   Navigate to the `/data` folder in the project's root directory.
    -   Copy and paste all your gathered files directly into this folder.

    **Example `/data` folder structure:**
    ```
    /data/
    ├── evacuation_routes.pdf
    ├── fire_safety_protocol.md
    ├── school_map_with_assembly_points.png
    └── lockdown_instructions.txt
    ```

3.  **Re-run the Ingestion Pipeline:**
    After adding, updating, or deleting any files in the `/data` directory, you **must** re-index the knowledge base. This process reads all the documents, chunks them, generates embeddings, and stores them in the vector database (ChromaDB/FAISS).

    -   Open your terminal.
    -   Make sure your virtual environment is activated (`source venv/bin/activate`).
    -   Run the following command from the project's root directory:

        ```bash
        python -m rag.ingest
        ```

    -   The script will process the new data. Once it's finished, the AI will use the updated knowledge base during interviews.

---

## 2. How to Customize Interview Questions

The interview questions are stored as individual Markdown files in the `/questions` directory. The application randomly selects 4 out of the total available questions.

### Structure of a Question Markdown File

Each `.md` file in the `/questions` directory follows a specific structure. You can edit these or create new ones using the same format.

Let's look at an example, `question_01.md`:

```markdown
---
id: 1
category: "Fire Safety"
---

### Scenario
You are in the school library on the second floor when you hear the fire alarm. You don't see or smell smoke, but the alarm is loud and continuous.

### Question
What are your immediate actions? Describe the steps you would take from hearing the alarm until you reach a designated safe area.

---

### Evaluation Rubric

#### Ideal Concepts to Mention:
- **Immediate Action:** Stop what you're doing immediately. Do not waste time gathering personal belongings.
- **Evacuation:** Proceed to the nearest fire exit. Do not use the elevator.
- **Safety Checks:** Before opening a door, feel it with the back of your hand. If it's hot, do not open it and find an alternate route.
- **Movement:** Stay low to the ground if you encounter smoke.
- **Assembly Point:** Go directly to the designated assembly point for the library.
- **Communication:** Remain quiet to hear instructions from teachers or staff. Do not shout or cause panic.

#### Dangerous Misconceptions:
- "I would wait for a teacher to tell me what to do." (Proactive movement is key).
- "I would grab my laptop and bag first." (Personal belongings are not a priority).
- "I would use the elevator to get down quickly." (Elevators are a death trap in a fire).
- "I would call my parents immediately." (This can jam networks and should wait until you are safe).
- "It's probably a drill, so I would just wait and see." (Always treat an alarm as real).

---

### Follow-up Guidance

- **If the user mentions waiting:** "Why is it important to act immediately rather than waiting for a teacher in this scenario?"
- **If the user mentions belongings:** "What is the primary risk of trying to save personal items during a fire alarm?"
- **If the user gives a vague answer:** "Can you be more specific about the route? How would you check if a door is safe to open?"
```

### How to Add a New Question:

1.  **Create a New File:**
    -   In the `/questions` directory, create a new file. Name it sequentially, e.g., `question_13.md`.

2.  **Follow the Format:**
    -   Copy the structure from an existing question file.
    -   **Front Matter (the `---` block at the top):**
        -   `id`: A unique number for the question.
        -   `category`: The disaster category it belongs to (e.g., "Earthquake," "Cybersecurity," "Lockdown").
    -   **Scenario & Question:** Write a clear, concise scenario and the question you want to ask the user.
    -   **Evaluation Rubric:**
        -   `Ideal Concepts`: List the key points a good answer should include. This is what the AI will look for.
        -   `Dangerous Misconceptions`: List common but incorrect actions. The AI will use this to identify critical safety gaps.
    -   **Follow-up Guidance:** Provide sample questions for the AI to ask if the user's answer is weak or contains a misconception.

3.  **Save the File:**
    -   Save the new markdown file in the `/questions` directory. The application will automatically discover it the next time it starts. No re-indexing is needed for changing questions.

By keeping your data and questions up-to-date, you ensure the "TSRS Moulsari AI Disaster Preparedness Evaluator" remains a relevant and effective tool for your school community.
