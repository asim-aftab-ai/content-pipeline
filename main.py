"""
CLI Runner for Content Pipeline with OpenRouter.
Demonstrates the 3-step prompt chaining workflow via command line.
"""

import sys
from content_pipeline import run_pipeline, get_openrouter_credentials


def main():
    print("==================================================")
    print("     Content Creation Pipeline (OpenRouter CLI)   ")
    print("==================================================")

    api_key, model = get_openrouter_credentials()
    if not api_key:
        print("\nNotice: OPENROUTER_API_KEY is not set in environment or .env.")
        print("To configure:")
        print("  1. Copy .env.example to .env:")
        print("     Copy-Item .env.example .env")
        print("  2. Add your key inside .env:")
        print("     OPENROUTER_API_KEY=your_key_here")
        print("     OPENROUTER_MODEL=openai/gpt-4o-mini")
        print("  3. Run Streamlit:")
        print("     uv run streamlit run app.py\n")
        return

    topic = input("Enter a topic (or press Enter for default: 'The Future of Renewable Energy'): ").strip()
    if not topic:
        topic = "The Future of Renewable Energy"

    print(f"\nModel: {model}")
    print(f"Topic: {topic}\n")

    try:
        print("[1/3] Running Step 1: Generating Outline via OpenRouter...")
        pipeline_data = run_pipeline(topic=topic, api_key=api_key, model=model)

        print("\n--- [Step 1 Output: Outline] ---")
        print(pipeline_data["step_1"]["output"][:300] + "...\n")

        print("[2/3] Running Step 2: Expanding Outline Points via OpenRouter...")
        print("\n--- [Step 2 Output: Expanded Content] ---")
        print(pipeline_data["step_2"]["output"][:300] + "...\n")

        print("[3/3] Running Step 3: Generating Final Summary via OpenRouter...")
        print("\n==================================================")
        print("                  FINAL OUTPUT                    ")
        print("==================================================")
        print(pipeline_data["final_output"])
        print("==================================================")

    except Exception as e:
        print(f"\nError running pipeline: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
