# Content Creation Pipeline

An educational demonstration of **Prompt Chaining** and **Sequential AI Processing** built with Python and Streamlit.

---

## 1. What This Project Does

This project demonstrates how to build an automated, multi-step AI pipeline where the output of one Large Language Model (LLM) stage becomes the direct input for the subsequent stage. 

Instead of asking an AI to do everything at once in a single massive prompt, the application breaks content generation down into three focused, manageable steps:

1. **Outline Generation**
2. **Section Expansion**
3. **Executive Summarization**

The Streamlit web interface makes this flow visually explicit so learners can observe how data is transformed at each step.

---

## 2. What Prompt Chaining Means

**Prompt Chaining** is a fundamental AI engineering pattern where multiple prompts are linked sequentially. 

Rather than sending one complex instruction to an LLM, prompt chaining decomposes the task into a series of smaller prompts where:
- Prompt 1 takes raw user input and produces Output 1.
- Prompt 2 takes Output 1 as its input and produces Output 2.
- Prompt 3 takes Output 2 as its input and produces Output 3 (the final output).

This approach ensures predictable quality, simpler debugging, and modular prompt maintenance.

---

## 3. The 3 Pipeline Stages

The pipeline consists of three distinct stages:

### Step 1: Generate Outline (`generate_outline`)
- **Role:** Content Planner.
- **Input:** Raw topic string entered by the user (e.g., *"The Impact of Quantum Computing on Cybersecurity"*).
- **Prompt Goal:** Create a clear, structured outline with 3-4 key sections and sub-points.
- **Output:** A structured outline.

### Step 2: Expand Each Point (`expand_outline`)
- **Role:** Technical Content Writer.
- **Input:** The generated outline from Step 1.
- **Prompt Goal:** Elaborate on each section of the outline, producing complete, detailed paragraphs.
- **Output:** Fully written, comprehensive article content.

### Step 3: Generate Final Summary (`generate_summary`)
- **Role:** Executive Editor.
- **Input:** The expanded article content from Step 2.
- **Prompt Goal:** Synthesize the detailed article into a concise executive summary with core takeaways.
- **Output:** A high-level executive summary and 3 key takeaways.

---

## 4. How Information Flows Between Stages

The core architecture follows a strict sequential data flow:

```
                  User Topic
                      |
                      v
        +---------------------------+
        |   generate_outline()      |  <-- Stage 1
        +---------------------------+
                      |
                   outline
                      |
                      v
        +---------------------------+
        |     expand_outline()      |  <-- Stage 2
        +---------------------------+
                      |
              expanded_content
                      |
                      v
        +---------------------------+
        |    generate_summary()     |  <-- Stage 3
        +---------------------------+
                      |
                final_summary
```

In Python code, this data flow is written explicitly without hidden layers:

```python
# Stage 1: Generate outline from user topic
outline = generate_outline(topic)

# Stage 2: Expand outline (Input is output of Stage 1)
expanded_content = expand_outline(outline)

# Stage 3: Generate summary (Input is output of Stage 2)
final_summary = generate_summary(expanded_content)
```

---

## 5. Why Use Multiple AI Stages Instead of One Large Prompt?

Attempting to do everything in a single prompt (*"Write an outline, expand it into full content, and then summarize it all in one response"*) often causes several problems:

1. **Cognitive Load & Attention Dilution:** LLMs can lose focus on specific constraints when given too many instructions simultaneously.
2. **Lower Output Depth:** When an LLM must generate an outline, full article, and summary in a single turn, it tends to truncate each section to stay within output limits.
3. **Lack of Inspectability:** In a single prompt, you cannot inspect or review intermediate steps (e.g., verifying if the outline is accurate before generating 1,000 words).
4. **Independent Tuning:** With prompt chaining, you can tweak temperature, persona, or prompt wording for one step without affecting the others.

---

## 6. Where Normal Software Could Be Used Instead of an LLM

Not every step in a pipeline needs an AI model. In production systems, software logic can replace or augment LLM steps:

- **Input Validation & Sanitization:** Regular expressions or schema validators (like Pydantic) to verify topic length, safety, or formatting.
- **Outline Parsing & Structure:** Splitting headings with string operations or regex rather than asking an LLM to parse them.
- **Grammar & Spell Checking:** Deterministic tools or linting engines (e.g., LanguageTool, Vale).
- **Keyword & SEO Tag Extraction:** Algorithmic extractors (e.g., TF-IDF, RAKE, YAKE) or database lookups.
- **Caching & Deduplication:** Redis or SQLite caching to return previously generated outlines instantly without burning API tokens.

---

## 7. Why Some Workflows are Sequential While Others are Parallel

- **Sequential Workflows (This Project):**
  - Used when **dependency is strict**: Step B cannot execute until Step A has completed.
  - In our pipeline, you cannot expand an outline that does not exist yet, nor can you summarize content before it has been written.
  
- **Parallel Workflows:**
  - Used when **steps are independent**: Multiple operations can run simultaneously on the same input data.
  - *Example:* Once the outline is ready, you could simultaneously generate:
    - Section 1 content (Worker 1)
    - Section 2 content (Worker 2)
    - Section 3 content (Worker 3)
  - Another example: Taking an article and simultaneously translating it into Spanish, French, and German.

---

## 8. How to Install Dependencies

The project uses `uv` (recommended) or standard `pip`.

### Using `uv`:
```powershell
uv pip install -r requirements.txt
```

### Using standard `pip`:
```powershell
pip install -r requirements.txt
```

---

## 9. How to Configure the API Key

The application supports both **Google Gemini** (default) and **OpenAI**.

### Option A: Using a `.env` file (Recommended)
1. Copy the example environment file:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Open `.env` and paste your key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```
   *(Or `OPENAI_API_KEY=your_actual_openai_key_here` if using OpenAI)*

### Option B: Setting the Environment Variable in Terminal
- **PowerShell:**
  ```powershell
  $env:GEMINI_API_KEY="your_api_key_here"
  ```
- **Bash / macOS / Linux:**
  ```bash
  export GEMINI_API_KEY="your_api_key_here"
  ```

### Option C: Entering in the Streamlit Sidebar
You can also launch the app and enter your key directly into the secure password field in the sidebar.

---

## 10. How to Run the Streamlit Application

Activate your virtual environment and start the Streamlit server:

```powershell
uv run streamlit run app.py
```

Or using the virtual environment's Python directly:
```powershell
.venv\Scripts\streamlit run app.py
```

Once running, open your browser at the local address (typically `http://localhost:8501`).

Enter a topic, click **Run Content Pipeline**, and observe each stage receive the previous stage's output.
