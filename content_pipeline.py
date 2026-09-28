"""
Content Creation Pipeline using OpenRouter
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

Every stage passes its actual output into the next OpenRouter request.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from openai import OpenAI

# Load local .env file if present
load_dotenv()

# Sensible default OpenRouter model if not overridden by OPENROUTER_MODEL
DEFAULT_MODEL = "openai/gpt-4o-mini"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def get_openrouter_credentials() -> tuple[Optional[str], str]:
    """
    Reads OpenRouter API key and model from environment variables.
    Returns:
        tuple[Optional[str], str]: (api_key, model_name)
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL") or DEFAULT_MODEL
    return api_key, model


def call_openrouter(
    prompt: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    """
    Sends a prompt to OpenRouter's OpenAI-compatible chat completion endpoint.

    Args:
        prompt: The text prompt for the LLM.
        api_key: Optional API key override. If None, reads OPENROUTER_API_KEY.
        model: Optional model override. If None, reads OPENROUTER_MODEL or defaults.

    Returns:
        str: Clean text content produced by the model.
    """
    env_key, env_model = get_openrouter_credentials()
    active_key = api_key or env_key
    active_model = model or env_model

    if not active_key:
        raise ValueError(
            "OPENROUTER_API_KEY is not configured. Please set the OPENROUTER_API_KEY "
            "environment variable in your .env file or enter it in the application sidebar."
        )

    try:
        client = OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=active_key,
        )

        response = client.chat.completions.create(
            model=active_model,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content
        if not content:
            raise RuntimeError(f"OpenRouter returned an empty response using model '{active_model}'.")

        return content.strip()

    except Exception as error:
        raise RuntimeError(f"OpenRouter API request failed: {str(error)}") from error


# ---------------------------------------------------------------------------
# PIPELINE STAGES
# ---------------------------------------------------------------------------


def generate_outline(
    topic: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    """
    STAGE 1: Generate Outline
    Takes the user topic and prompts OpenRouter to create a structured outline.

    Input:
        topic (str): The subject entered by the user.
    Output:
        outline (str): A structured, multi-section outline.
    """
    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty. Please provide a valid topic.")

    prompt = f"""You are a professional content planner.
Create a structured outline for an informative article on the following topic.

Topic: {topic.strip()}

Instructions:
- Provide 3 to 4 major sections or key headings.
- Under each section, include 2 concise sub-points or talking points.
- Keep the outline clear, logical, and well-structured."""

    return call_openrouter(prompt, api_key=api_key, model=model)


def expand_outline(
    outline: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    """
    STAGE 2: Expand Each Point
    Takes the outline produced by Stage 1 and prompts OpenRouter to write full paragraphs.

    Input:
        outline (str): The actual output from Stage 1.
    Output:
        expanded_content (str): Complete, detailed article sections.
    """
    if not outline or not outline.strip():
        raise ValueError("Outline cannot be empty. Stage 1 must generate content first.")

    prompt = f"""You are an expert technical content writer.
Take the structured outline provided below and expand each point into comprehensive, engaging article paragraphs.

Outline:
{outline.strip()}

Instructions:
- Expand every section and sub-point with clear, detailed explanations.
- Ensure smooth transitions between paragraphs.
- Write full, thorough paragraphs without summarizing yet."""

    return call_openrouter(prompt, api_key=api_key, model=model)


def generate_summary(
    expanded_content: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    """
    STAGE 3: Generate Final Summary
    Takes the expanded article from Stage 2 and prompts OpenRouter to synthesize an executive summary.

    Input:
        expanded_content (str): The actual output from Stage 2.
    Output:
        final_summary (str): A concise executive summary with key takeaways.
    """
    if not expanded_content or not expanded_content.strip():
        raise ValueError("Expanded content cannot be empty. Stage 2 must generate content first.")

    prompt = f"""You are an executive editor.
Review the detailed content below and produce a concise executive summary.

Content:
{expanded_content.strip()}

Instructions:
- Write a 2-3 sentence overarching overview.
- List exactly 3 key takeaways as clear bullet points.
- Keep the tone professional, objective, and crisp."""

    return call_openrouter(prompt, api_key=api_key, model=model)


def run_pipeline(
    topic: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Executes the sequential 3-step prompt chain using OpenRouter:

        topic
          |
        outline = generate_outline(topic)
          |
        expanded_content = expand_outline(outline)
          |
        final_summary = generate_summary(expanded_content)

    Returns a dictionary containing stage names, descriptions, inputs, and outputs.
    """
    # Step 1: Generate Outline
    outline = generate_outline(topic, api_key=api_key, model=model)

    # Step 2: Expand Outline (Input is the direct output from Step 1)
    expanded_content = expand_outline(outline, api_key=api_key, model=model)

    # Step 3: Generate Summary (Input is the direct output from Step 2)
    final_summary = generate_summary(expanded_content, api_key=api_key, model=model)

    return {
        "topic": topic,
        "step_1": {
            "name": "Step 1: Generate Outline",
            "description": "Takes the user topic and prompts OpenRouter to produce a structured outline.",
            "input": topic,
            "output": outline,
        },
        "step_2": {
            "name": "Step 2: Expand Each Point",
            "description": "Takes the outline from Step 1 as input and prompts OpenRouter to write comprehensive paragraphs.",
            "input": outline,
            "output": expanded_content,
        },
        "step_3": {
            "name": "Step 3: Generate Final Summary",
            "description": "Takes the expanded content from Step 2 as input and prompts OpenRouter to create a concise executive summary.",
            "input": expanded_content,
            "output": final_summary,
        },
        "final_output": final_summary,
    }
