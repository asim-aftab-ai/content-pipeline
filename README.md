# Content Creation Pipeline (Powered by OpenRouter)

An educational demonstration of **Prompt Chaining** and **Sequential AI Processing** built with Python, Streamlit, and **OpenRouter**.

---

## 1. What This Project Does

This project demonstrates how to build an automated, multi-step AI pipeline where the output of one Large Language Model (LLM) stage becomes the direct input for the subsequent stage. 

All LLM calls are routed through **OpenRouter**, providing a unified, OpenAI-compatible API endpoint to access a wide variety of models.

Instead of asking an AI to do everything in a single massive prompt, the pipeline breaks content creation into three focused, manageable steps:

1. **Step 1: Generate Outline**
2. **Step 2: Expand Each Point**
3. **Step 3: Generate Final Summary**

The Streamlit web interface makes this sequence visually explicit so learners can observe how data is transformed at each step.

---

## 2. What Prompt Chaining Means

**Prompt Chaining** is a foundational AI engineering pattern where multiple prompts are linked sequentially.

Rather than sending one overloaded prompt to an LLM, prompt chaining decomposes the task into smaller, highly specialized prompts where:
- Prompt 1 takes raw user input and produces Output 1.
- Prompt 2 takes Output 1 as its input and produces Output 2.
- Prompt 3 takes Output 2 as its input and produces Output 3 (the final output).

This approach ensures higher reliability, simpler debugging, and modular prompt maintenance.

---

## 3. The 3 Pipeline Stages

### Step 1: Generate Outline (`generate_outline`)
- **Role:** Content Planner.
- **Input:** Raw topic entered by the user (e.g., *"The Impact of Quantum Computing on Cybersecurity"*).
- **Prompt Goal:** Create a clear, structured outline with 3-4 key sections and sub-points.
- **Output:** A structured outline.

### Step 2: Expand Each Point (`expand_outline`)
- **Role:** Technical Content Writer.
- **Input:** The generated outline from Step 1.
- **Prompt Goal:** Elaborate on each point of the outline, producing complete, detailed paragraphs.
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
        |   generate_outline()      |  <-- Stage 1 (OpenRouter)
        +---------------------------+
                      |
                   outline
                      |
                      v
        +---------------------------+
        |     expand_outline()      |  <-- Stage 2 (OpenRouter)
        +---------------------------+
                      |
              expanded_content
                      |
                      v
        +---------------------------+
        |    generate_summary()     |  <-- Stage 3 (OpenRouter)
        +---------------------------+
                      |
                final_summary
```

In `content_pipeline.py`, this data flow is written explicitly without hidden layers:

```python
# Stage 1: Generate outline from user topic
outline = generate_outline(topic)

# Stage 2: Expand outline (Input is output of Stage 1)
expanded_content = expand_outline(outline)

# Stage 3: Generate summary (Input is output of Stage 2)
final_summary = generate_summary(expanded_content)
```

---

## 5. OpenRouter Configuration

This project uses **OpenRouter** (`https://openrouter.ai/api/v1`) via the OpenAI-compatible client.

### Where the OpenRouter API Key is Configured
The API key is read from an environment variable named:
```env
OPENROUTER_API_KEY
```
Never hardcode API keys in the source code. Instead, configure it in a local `.env` file (which is excluded from Git via `.gitignore`).

### What `OPENROUTER_MODEL` Does
`OPENROUTER_MODEL` specifies which model OpenRouter should execute for all pipeline stages.
- If specified (e.g., `openai/gpt-4o-mini`, `google/gemini-2.0-flash-001`, `anthropic/claude-3.5-haiku`), OpenRouter routes calls to that specific model.
- If not specified, the project automatically defaults to:
  ```python
  DEFAULT_MODEL = "openai/gpt-4o-mini"
  ```

---

## 6. How to Install Dependencies

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

## 7. How to Configure the Environment

1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Open `.env` and set your OpenRouter API key and desired model:
   ```env
   OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
   OPENROUTER_MODEL=openai/gpt-4o-mini
   ```

You can also input or override your API key directly in the Streamlit sidebar.

---

## 8. How to Run the Application

### Streamlit Web App:
```powershell
uv run streamlit run app.py
```
Or with virtual environment Python:
```powershell
.venv\Scripts\streamlit run app.py
```

### Command Line Interface (CLI):
```powershell
uv run python main.py
```

---

## 9. Error Handling

- **Missing API Key:** If `OPENROUTER_API_KEY` is not found, Streamlit displays a clear error warning explaining that the key must be configured in `.env` or the sidebar.
- **Empty Topic:** Prevents API calls and prompts the user to enter a valid topic.
- **API Request Failure:** Any network or model errors from OpenRouter are intercepted and displayed in human-readable alerts rather than crashing the interface.
