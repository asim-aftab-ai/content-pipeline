"""
CLI Runner for Content Pipeline.
Demonstrates the 3-step prompt chaining workflow via command line.
"""

import sys
from content_pipeline import run_pipeline, get_configured_provider


def main():
    print("==================================================")
    print("        Content Creation Pipeline (CLI)          ")
    print("==================================================")

    provider, api_key = get_configured_provider()
    if not api_key:
        print("\nNotice: No API key detected in environment (GEMINI_API_KEY or OPENAI_API_KEY).")
        print("To run the full pipeline:")
        print("  1. Set your API key in a .env file or environment variable:")
        print("     export GEMINI_API_KEY=\"your_key_here\"  # or set in PowerShell: $env:GEMINI_API_KEY=\"your_key\"")
        print("  2. Launch the Streamlit interface:")
        print("     uv run streamlit run app.py\n")
        return

    topic = input("Enter a topic (or press Enter for default: 'The Future of Renewable Energy'): ").strip()
    if not topic:
        topic = "The Future of Renewable Energy"

    print(f"\nSelected Provider: {provider}")
    print(f"Topic: {topic}\n")

    try:
        print("[1/3] Running Step 1: Generating Outline...")
        pipeline_data = run_pipeline(topic=topic, provider=provider, api_key=api_key)

        print("\n--- [Step 1 Output: Outline] ---")
        print(pipeline_data["step_1"]["output"][:300] + "...\n")

        print("[2/3] Running Step 2: Expanding Outline Points...")
        print("\n--- [Step 2 Output: Expanded Content] ---")
        print(pipeline_data["step_2"]["output"][:300] + "...\n")

        print("[3/3] Running Step 3: Generating Final Summary...")
        print("\n==================================================")
        print("                  FINAL OUTPUT                    ")
        print("==================================================")
        print(pipeline_data["final_output"])
        print("==================================================")

    except Exception as e:
        print(f"\nError running pipeline: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
