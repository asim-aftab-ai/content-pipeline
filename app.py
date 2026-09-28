"""
Streamlit Application: 3-Step Content Creation Pipeline
Demonstrates Prompt Chaining where the output of each stage becomes the input to the next.
"""

import os
import streamlit as st
from content_pipeline import (
    generate_outline,
    expand_outline,
    generate_summary,
    get_configured_provider,
)

# Page configuration - strictly NO emojis anywhere
st.set_page_config(
    page_title="Content Creation Pipeline",
    layout="wide",
)

st.title("Content Creation Pipeline")
st.caption("Educational demonstration of Prompt Chaining and Sequential AI Processing")

st.markdown(
    """
This application demonstrates **Prompt Chaining**: a multi-stage workflow where an LLM is called sequentially, 
and the output of each stage serves as the direct input to the next stage.
"""
)

# Visual Architecture Flow
with st.container():
    st.markdown("### Pipeline Architecture")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.info("**User Input**\nEnter Topic")
    with col2:
        st.info("**Step 1**\nGenerate Outline")
    with col3:
        st.info("**Step 2**\nExpand Points")
    with col4:
        st.info("**Step 3**\nFinal Summary")
    with col5:
        st.success("**Final Output**\nExecutive Summary")

st.divider()

# Sidebar: API Configuration
st.sidebar.header("Configuration")

detected_provider, env_key = get_configured_provider()

provider_options = ["gemini", "openai"]
default_provider_index = 0 if detected_provider != "openai" else 1

selected_provider = st.sidebar.selectbox(
    "LLM Provider",
    options=provider_options,
    index=default_provider_index,
    format_func=lambda x: "Google Gemini (gemini-2.5-flash)" if x == "gemini" else "OpenAI (gpt-4o-mini)",
    help="Select the AI provider to power each pipeline stage.",
)

api_key_input = st.sidebar.text_input(
    f"{selected_provider.upper()} API Key",
    type="password",
    value=env_key if (env_key and detected_provider == selected_provider) else "",
    help=f"Enter your {selected_provider.upper()} API key or set it in your .env / environment variables.",
)

if api_key_input:
    st.sidebar.caption(f"Status: API key provided for {selected_provider.capitalize()}.")
else:
    st.sidebar.warning(
        f"Status: No API key found. Enter a key above or set {selected_provider.upper()}_API_KEY in your environment."
    )

st.sidebar.divider()
st.sidebar.markdown(
    """
**Educational Notes**
- **Stage 1 Input**: User Topic
- **Stage 2 Input**: Stage 1 Outline
- **Stage 3 Input**: Stage 2 Expanded Text
- **Final Output**: Stage 3 Summary
"""
)

# Main Application Interface
st.subheader("Topic Input")
topic_input = st.text_input(
    "Enter a topic for the content pipeline:",
    placeholder="e.g., The Future of Electric Aviation",
)

col_run, col_clear = st.columns([1, 5])
with col_run:
    run_button = st.button("Run Content Pipeline", type="primary")
with col_clear:
    if st.button("Clear Results"):
        st.session_state.pop("pipeline_results", None)
        st.rerun()

# Execute Pipeline
if run_button:
    if not topic_input or not topic_input.strip():
        st.error("Please enter a topic before starting the pipeline.")
    elif not api_key_input or not api_key_input.strip():
        st.error(
            f"Missing API key. Please enter a valid {selected_provider.upper()} API key in the sidebar or configure your environment variables."
        )
    else:
        results = {}
        progress_placeholder = st.empty()

        try:
            # Stage 1: Generate Outline
            with progress_placeholder.container():
                st.info("Executing Step 1: Generating structured outline from topic...")
            outline = generate_outline(
                topic=topic_input.strip(),
                api_key=api_key_input.strip(),
                provider=selected_provider,
            )
            results["step_1"] = {
                "name": "STEP 1: Generate Outline",
                "explanation": "Takes the raw topic and asks the LLM to create a structured outline with key sections.",
                "input": topic_input.strip(),
                "output": outline,
            }

            # Stage 2: Expand Outline
            with progress_placeholder.container():
                st.info("Executing Step 2: Expanding each outline point into full content...")
            expanded_content = expand_outline(
                outline=outline,
                api_key=api_key_input.strip(),
                provider=selected_provider,
            )
            results["step_2"] = {
                "name": "STEP 2: Expand Each Point",
                "explanation": "Takes the outline from Step 1 as input and asks the LLM to write detailed paragraphs for each section.",
                "input": outline,
                "output": expanded_content,
            }

            # Stage 3: Generate Summary
            with progress_placeholder.container():
                st.info("Executing Step 3: Synthesizing final executive summary from expanded content...")
            final_summary = generate_summary(
                expanded_content=expanded_content,
                api_key=api_key_input.strip(),
                provider=selected_provider,
            )
            results["step_3"] = {
                "name": "STEP 3: Generate Final Summary",
                "explanation": "Takes the full expanded content from Step 2 as input and asks the LLM to synthesize a concise summary.",
                "input": expanded_content,
                "output": final_summary,
            }

            results["topic"] = topic_input.strip()
            results["final_output"] = final_summary
            st.session_state["pipeline_results"] = results
            progress_placeholder.empty()

        except Exception as error:
            progress_placeholder.empty()
            st.error(f"Pipeline execution stopped due to an error: {str(error)}")

# Render Pipeline Stages
if "pipeline_results" in st.session_state:
    data = st.session_state["pipeline_results"]

    st.markdown("---")
    st.subheader("Pipeline Execution Stages")
    st.caption("Follow the arrows to see how each stage output transfers to the next stage input.")

    # STEP 1
    with st.container():
        st.markdown(f"#### {data['step_1']['name']}")
        st.write(f"**Explanation:** {data['step_1']['explanation']}")

        col_in, col_out = st.columns(2)
        with col_in:
            st.markdown("**Stage Input (User Topic):**")
            st.text_area(
                "Step 1 Input",
                value=data["step_1"]["input"],
                height=150,
                disabled=True,
                key="view_step1_in",
                label_visibility="collapsed",
            )
        with col_out:
            st.markdown("**Stage Output (Generated Outline):**")
            st.text_area(
                "Step 1 Output",
                value=data["step_1"]["output"],
                height=150,
                disabled=True,
                key="view_step1_out",
                label_visibility="collapsed",
            )

    # Transition 1 -> 2
    st.markdown(
        """
        <div style="text-align: center; margin: 15px 0;">
            <p style="font-weight: bold; color: #4B5563; margin-bottom: 2px;">
                | Output of Step 1 becomes Input to Step 2
            </p>
            <p style="font-size: 22px; font-weight: bold; margin: 0;">v</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # STEP 2
    with st.container():
        st.markdown(f"#### {data['step_2']['name']}")
        st.write(f"**Explanation:** {data['step_2']['explanation']}")

        col_in, col_out = st.columns(2)
        with col_in:
            st.markdown("**Stage Input (Outline from Step 1):**")
            st.text_area(
                "Step 2 Input",
                value=data["step_2"]["input"],
                height=250,
                disabled=True,
                key="view_step2_in",
                label_visibility="collapsed",
            )
        with col_out:
            st.markdown("**Stage Output (Expanded Content):**")
            st.text_area(
                "Step 2 Output",
                value=data["step_2"]["output"],
                height=250,
                disabled=True,
                key="view_step2_out",
                label_visibility="collapsed",
            )

    # Transition 2 -> 3
    st.markdown(
        """
        <div style="text-align: center; margin: 15px 0;">
            <p style="font-weight: bold; color: #4B5563; margin-bottom: 2px;">
                | Output of Step 2 becomes Input to Step 3
            </p>
            <p style="font-size: 22px; font-weight: bold; margin: 0;">v</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # STEP 3
    with st.container():
        st.markdown(f"#### {data['step_3']['name']}")
        st.write(f"**Explanation:** {data['step_3']['explanation']}")

        col_in, col_out = st.columns(2)
        with col_in:
            st.markdown("**Stage Input (Expanded Content from Step 2):**")
            st.text_area(
                "Step 3 Input",
                value=data["step_3"]["input"],
                height=200,
                disabled=True,
                key="view_step3_in",
                label_visibility="collapsed",
            )
        with col_out:
            st.markdown("**Stage Output (Final Summary):**")
            st.text_area(
                "Step 3 Output",
                value=data["step_3"]["output"],
                height=200,
                disabled=True,
                key="view_step3_out",
                label_visibility="collapsed",
            )

    # Transition 3 -> Final
    st.markdown(
        """
        <div style="text-align: center; margin: 15px 0;">
            <p style="font-weight: bold; color: #4B5563; margin-bottom: 2px;">
                | Pipeline Completed
            </p>
            <p style="font-size: 22px; font-weight: bold; margin: 0;">v</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # FINAL OUTPUT SECTION
    st.markdown("### Final Content Output")
    with st.expander("View Final Generated Summary", expanded=True):
        st.markdown(data["final_output"])
