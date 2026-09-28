"""
Content Creation Pipeline
Demonstrating Prompt Chaining and Sequential AI Processing.

Pipeline Data Flow:
    topic
      |
      v
    outline = generate_outline(topic)
      |
      v
    expanded_content = expand_outline(outline)
      |
      v
    final_summary = generate_summary(expanded_content)

The output of each stage becomes the direct input to the subsequent stage.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from a local .env file if present
load_dotenv()


def get_configured_provider() -> tuple[Optional[str], Optional[str]]:
    """
    Checks environment variables to detect configured API keys.
    Returns a tuple of (provider_name, api_key).
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if gemini_key:
        return "gemini", gemini_key
    if openai_key:
        return "openai", openai_key
    return None, None


def call_llm(
    prompt: str,
    api_key: Optional[str] = None,
    provider: Optional[str] = None,
) -> str:
    """
    Minimal helper to send a prompt to an LLM provider and return the text response.
    Supports Google Gemini (default) and OpenAI.
    """
    # Detect provider and key if not explicitly passed
    detected_provider, env_key = get_configured_provider()
    active_key = api_key or env_key
    active_provider = provider or detected_provider or "gemini"

    if not active_key:
        raise ValueError(
            "API key not found. Please provide an API key in the UI or set the "
            "GEMINI_API_KEY (or OPENAI_API_KEY) environment variable."
        )

    if active_provider == "gemini":
        try:
            from google import genai
            client = genai.Client(api_key=active_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            if not response.text:
                raise RuntimeError("Gemini returned an empty response.")
            return response.text.strip()
        except Exception as e:
            raise RuntimeError(f"Gemini API request failed: {str(e)}") from e

    elif active_provider == "openai":
        try:
            from openai import OpenAI
            client = OpenAI(api_key=active_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            content = response.choices[0].message.content
            if not content:
                raise RuntimeError("OpenAI returned an empty response.")
            return content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI API request failed: {str(e)}") from e

    else:
        raise ValueError(f"Unsupported provider: {active_provider}")


# ---------------------------------------------------------------------------
# PIPELINE STAGES
# ---------------------------------------------------------------------------


def generate_outline(
    topic: str,
    api_key: Optional[str] = None,
    provider: Optional[str] = None,
) -> str:
    """
    STAGE 1: Generate Outline
    Takes the user's topic and requests a structured outline from the LLM.

    Input:
        topic (str): The subject entered by the user.
    Output:
        outline (str): A structured, multi-section outline.
    """
    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty. Please provide a valid topic.")

    prompt = f"""You are a professional content planner.
Create a structured outline for an article on the following topic.

Topic: {topic.strip()}

Instructions:
- Provide 3 to 4 key sections.
- Under each section, include 2 concise sub-points or talking points.
- Keep the outline clear, logical, and easy to expand."""

    return call_llm(prompt, api_key=api_key, provider=provider)


def expand_outline(
    outline: str,
    api_key: Optional[str] = None,
    provider: Optional[str] = None,
) -> str:
    """
    STAGE 2: Expand Each Point
    Takes the outline produced by Stage 1 and expands each point into detailed content.

    Input:
        outline (str): The structured outline produced by Stage 1.
    Output:
        expanded_content (str): The fully expanded article sections.
    """
    if not outline or not outline.strip():
        raise ValueError("Outline cannot be empty. Stage 1 must generate content first.")

    prompt = f"""You are an expert technical content writer.
Take the structured outline below and write out complete, detailed paragraphs for each section.

Outline to expand:
{outline.strip()}

Instructions:
- Expand every section and sub-point with clear, informative explanations.
- Maintain smooth transitions between sections.
- Write full, thorough paragraphs without summarizing yet."""

    return call_llm(prompt, api_key=api_key, provider=provider)


def generate_summary(
    expanded_content: str,
    api_key: Optional[str] = None,
    provider: Optional[str] = None,
) -> str:
    """
    STAGE 3: Generate Final Summary
    Takes the expanded article from Stage 2 and synthesizes a concise executive summary.

    Input:
        expanded_content (str): The detailed content produced by Stage 2.
    Output:
        final_summary (str): A concise summary with core takeaways.
    """
    if not expanded_content or not expanded_content.strip():
        raise ValueError("Expanded content cannot be empty. Stage 2 must generate content first.")

    prompt = f"""You are an executive editor.
Review the detailed content below and produce a concise executive summary.

Content to summarize:
{expanded_content.strip()}

Instructions:
- Provide a 2-3 sentence overarching summary.
- List exactly 3 key takeaways as concise bullet points.
- Keep the tone professional, objective, and crisp."""

    return call_llm(prompt, api_key=api_key, provider=provider)


def run_pipeline(
    topic: str,
    api_key: Optional[str] = None,
    provider: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Executes the entire 3-step prompt chain sequentially.

    Explicit Data Flow:
        topic
          |
        outline = generate_outline(topic)
          |
        expanded_content = expand_outline(outline)
          |
        final_summary = generate_summary(expanded_content)

    Returns a dictionary containing each stage's name, description, input, and output.
    """
    # Step 1: Generate Outline from user topic
    outline = generate_outline(topic, api_key=api_key, provider=provider)

    # Step 2: Expand the Outline (Input is the direct output of Step 1)
    expanded_content = expand_outline(outline, api_key=api_key, provider=provider)

    # Step 3: Generate Summary (Input is the direct output of Step 2)
    final_summary = generate_summary(expanded_content, api_key=api_key, provider=provider)

    return {
        "topic": topic,
        "step_1": {
            "name": "Step 1: Generate Outline",
            "description": "Takes the user topic and asks the LLM to generate a structured outline.",
            "input": topic,
            "output": outline,
        },
        "step_2": {
            "name": "Step 2: Expand Each Point",
            "description": "Takes the outline from Step 1 and asks the LLM to expand each point into full paragraphs.",
            "input": outline,
            "output": expanded_content,
        },
        "step_3": {
            "name": "Step 3: Generate Final Summary",
            "description": "Takes the expanded content from Step 2 and asks the LLM to create a concise final summary.",
            "input": expanded_content,
            "output": final_summary,
        },
        "final_output": final_summary,
    }
