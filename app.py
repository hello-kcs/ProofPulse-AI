

import os
import streamlit as st
from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()

st.set_page_config(
    page_title="ProofPulse AI",
    page_icon="🚀"
)

st.title("🚀 ProofPulse AI")
st.write("Turn conversations into actionable tasks!")

chat = st.text_area(
    "Paste conversation",
    """Rahul: Main kal tak frontend complete kar dunga.
Priya: Backend Sunday tak kar lungi.
Aman: Documentation ka dekh lenge.
Rahul: Actually frontend Monday tak hoga.""",
    height=200
)

if st.button("Analyze Commitments"):
    if not chat.strip():
        st.warning("Please enter a conversation.")
        st.stop()

    try:
        # Works locally using .env
        api_key = os.getenv("SARVAM_API_KEY")

        # Works on Streamlit Cloud using Secrets
        if not api_key:
            api_key = st.secrets.get("SARVAM_API_KEY")

        if not api_key:
            st.error("Sarvam API key is missing.")
            st.stop()

        client = SarvamAI(
            api_subscription_key=api_key
        )

        with st.spinner("Analyzing with Sarvam AI..."):
            response = client.chat.completions(
                model="sarvam-105b",
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "Analyze this conversation and extract "
                            "task owners, commitments, deadlines, "
                            "revised promises and unclear responsibilities. "
                            "Return a Markdown table and suggest "
                            "follow-up questions. "
                            "Do not invent facts or assume completion. "
                            "Conversation:\n\n" + chat
                        )
                    }
                ]
            )

        result = response.choices[0].message.content

        st.subheader("📋 Extracted Responsibilities")
        st.markdown(result)

        st.download_button(
            "📥 Download Report",
            data=result,
            file_name="proofpulse_report.md",
            mime="text/markdown"
        )

    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.caption("Powered by Sarvam AI")
