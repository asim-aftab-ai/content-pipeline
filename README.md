# Content Creation Pipeline (Powered by OpenRouter)

An educational reference project demonstrating **Prompt Chaining** and **Sequential AI Processing** built with Python, Streamlit, and **OpenRouter**.

---

## Overview

In practical AI engineering, asking a Large Language Model (LLM) to perform an entire creative or analytical workflow in a single monolithic prompt often produces shallow, unstructured, or truncated results. 

The **Content Creation Pipeline** demonstrates the solution: **Prompt Chaining**. The pipeline decomposes content generation into three discrete, focused stages where each stage executes a specific role, and the output of one stage directly feeds the next.

```
                  User Topic
                      |
                      v
        +---------------------------+
        |  Step 1: Generate Outline |  <-- OpenRouter LLM Call
        +---------------------------+
                      |
                   outline
                      |
                      v
        +---------------------------+
        |  Step 2: Expand Outline   |  <-- OpenRouter LLM Call
        +---------------------------+
                      |
              expanded_content
                      |
                      v
        +---------------------------+
        |  Step 3: Generate Summary |  <-- OpenRouter LLM Call
        +---------------------------+
                      |
                final_summary (Final Output)
```

The accompanying **Streamlit** user interface displays each stage's inputs, explanations, and outputs side-by-side, making the data handoff completely transparent.

---

## Core Concepts Demonstrated

### 1. What is Prompt Chaining?
Prompt Chaining is an architectural pattern in AI system design where complex tasks are broken down into sequential steps. Each step uses a dedicated prompt and the resulting model output is passed forward as contextual input into the next prompt.

### 2. Why Multiple Stages Instead of One Monolithic Prompt?
| Challenge with Single Prompts | How Prompt Chaining Solves It |
| :--- | :--- |
| **Attention Dilution**: Models forget earlier constraints when given multiple complex tasks at once. | Each prompt focuses on **one objective** (e.g. outline vs. prose vs. executive summary). |
| **Output Token Truncation**: Generating an outline, full article, and summary together easily hits output limits. | Each stage has its own complete response budget for maximum depth. |
| **Lack of Observability**: You cannot inspect intermediate steps if everything happens in one call. | Each stage output is inspectable, verifiable, and can be edited or validated before proceeding. |
| **Inflexible Model Tuning**: You cannot use different models or parameters for different tasks. | You can easily route outline planning to a reasoning model and summarization to a faster model. |

### 3. Where Traditional Software Replaces or Augments LLMs
In production pipelines, not every task requires an LLM. Pure software components should handle:
- **Input Validation**: Verifying topic length, formatting, and character sets using deterministic validation.
- **Parsing & Structuring**: Extracting sections, regex matching, and Markdown parsing.
- **Deduplication & Caching**: Storing generated outlines in Redis or SQLite to prevent redundant API calls.
- **Output Sanitization**: Cleaning unwanted tokens, enforcing schema compliance (e.g., Pydantic).

### 4. Sequential vs. Parallel Workflows
- **Sequential (This Pipeline)**: Step $N+1$ depends directly on the result of Step $N$. You cannot expand an outline before creating it, nor can you summarize content before it has been written.
- **Parallel Workflows**: Useful when sub-tasks are independent. For example, once the outline is ready, Sections A, B, and C could be expanded simultaneously across three parallel API calls.

---

## Pipeline Stages Breakdown

| Stage | Function | Persona / Role | Input | Output |
| :--- | :--- | :--- | :--- | :--- |
| **Step 1** | `generate_outline()` | Content Planner | Raw user topic string | 3–4 section structured outline with sub-points |
| **Step 2** | `expand_outline()` | Technical Writer | Stage 1 output (`outline`) | Thorough, multi-paragraph drafted article |
| **Step 3** | `generate_summary()` | Executive Editor | Stage 2 output (`expanded_content`) | High-impact overview and 3 key takeaways |

### Explicit Python Data Flow

The chaining logic is implemented cleanly in [`content_pipeline.py`](file:///f:/Projects/Month-02/Week-03/Project-01/Content-Pipeline/content_pipeline.py) without unnecessary abstraction:

```python
# Step 1: Takes user topic, outputs structured outline
outline = generate_outline(topic, api_key=api_key, model=model)

# Step 2: Takes outline from Step 1, outputs comprehensive content
expanded_content = expand_outline(outline, api_key=api_key, model=model)

# Step 3: Takes expanded content from Step 2, outputs concise executive summary
final_summary = generate_summary(expanded_content, api_key=api_key, model=model)
```

---

## Project Structure

```
Content-Pipeline/
├── .env.example          # Environment variable template
├── .gitignore            # Excludes .env, .venv, and build artifacts
├── app.py                # Clean Streamlit user interface (zero emojis)
├── content_pipeline.py   # Core 3-step prompt chaining logic
├── main.py               # Command-line interface (CLI) runner
├── pyproject.toml        # Project configuration and dependencies
├── requirements.txt      # Dependency specification
└── README.md             # Project documentation
```

---

## Installation & Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- An [OpenRouter API Key](https://openrouter.ai/keys)

### 1. Clone & Navigate to Repository
```powershell
git clone https://github.com/asim-aftab-ai/content-pipeline.git
cd content-pipeline
```

### 2. Install Dependencies
You can install using `uv` (recommended) or standard `pip`:

**Using `uv`:**
```powershell
uv pip install -r requirements.txt
```

**Using standard `pip`:**
```powershell
pip install -r requirements.txt
```

---

## Configuration

The application uses OpenRouter's OpenAI-compatible endpoint (`https://openrouter.ai/api/v1`).

### 1. Set Up Your Environment File
Copy the example file to `.env`:
```powershell
Copy-Item .env.example .env
```

### 2. Configure Your Keys in `.env`
Open `.env` and set your OpenRouter API key and preferred model:
```env
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
OPENROUTER_MODEL=openai/gpt-4o-mini
```

### Supported Models on OpenRouter
You can configure `OPENROUTER_MODEL` to any model available on OpenRouter, for example:
- `openai/gpt-4o-mini` *(default — fast and affordable)*
- `google/gemini-2.0-flash-001`
- `anthropic/claude-3.5-haiku`
- `deepseek/deepseek-chat`
- `meta-llama/llama-3.3-70b-instruct`

*(Note: You can also enter or override your API key directly in the Streamlit sidebar).*

---

## Running the Application

### Option A: Streamlit Web Interface (Recommended)
Launch the interactive web UI:
```powershell
uv run streamlit run app.py
```
Or directly with Python:
```powershell
python -m streamlit run app.py
```
Open your browser at `http://localhost:8501`. Enter a topic, click **Run Content Pipeline**, and watch each stage transform its input into the next stage's prompt.

### Option B: Command-Line Interface (CLI)
Run the pipeline directly from your terminal:
```powershell
uv run python main.py
```

---

## Error Handling

The pipeline includes built-in defensive validation:
- **Missing API Key**: Detects missing keys before making requests and displays a clear message directing the user to configure `.env` or use the sidebar.
- **Empty Topic Input**: Rejects empty queries with a helpful warning.
- **OpenRouter API Errors**: Catches upstream network issues or invalid model identifiers and renders human-readable error messages without crashing the Streamlit process.

---

## License & Credits

Built as part of the AI Engineering curriculum demonstrating sequential multi-step AI pipelines. Powered by [OpenRouter](https://openrouter.ai/).
