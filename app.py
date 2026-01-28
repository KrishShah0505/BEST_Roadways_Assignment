import streamlit as st
from extractor import extract_inquiry
from pydantic import ValidationError
import os

st.set_page_config(page_title="AI Inquiry Inbox – PRD Prototype", layout="wide")

st.title("📥 AI Inquiry Inbox — PRD Prototype")
st.markdown("### Convert unstructured logistics emails into structured RFQs using AI")

st.sidebar.title("📚 Sample Emails")

sample_dir = "data/sample_emails"
samples = {}

if os.path.exists(sample_dir):
    for fname in os.listdir(sample_dir):
        with open(os.path.join(sample_dir, fname), "r", encoding="utf-8") as f:
            samples[fname] = f.read()

selected_sample = st.sidebar.selectbox("Load sample:", [""] + list(samples.keys()))

if selected_sample:
    email_text = samples[selected_sample]

email_text = st.text_area("📧 Paste Inquiry Email Here", value=email_text if "email_text" in locals() else "", height=280)


colA, colB = st.columns([1, 5])
process_btn = colA.button("🚀 Process Inquiry")

if process_btn:
    if not email_text.strip():
        st.warning("Please paste an email first.")
    else:
        with st.spinner("Processing with AI..."):
            try:
                result = extract_inquiry(email_text)

                st.success("Processing Complete!")

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Is Inquiry", "Yes" if result.is_inquiry else "No")
                col2.metric("Needs Review", " YES" if result.needs_review else " NO")
                col3.metric("Line Items", len(result.line_items))
                col4.metric("Overall Confidence", f"{result.header.overall_confidence}%")

                st.divider()

                tab1, tab2, tab3 = st.tabs([" Structured JSON", " Line Items", " Confidence"])

                with tab1:
                    st.json(result.dict())
                    import json

                    st.download_button(
                        label="⬇️ Download JSON",
                        data=json.dumps(result.dict(), indent=2),
                        file_name="parsed_inquiry.json",
                        mime="application/json"
                    )


                with tab2:
                    if result.line_items:
                        rows = []
                        for li in result.line_items:
                            d = li.dict()
                            d["vehicle_type_normalized"] = li.vehicle_type_normalized
                            rows.append(d)
                        st.dataframe(rows, use_container_width=True)
                    else:
                        st.info("No line items extracted.")

                with tab3:
                    if result.line_items:
                        for i, li in enumerate(result.line_items, 1):
                            st.subheader(f"Line Item {i}")
                            st.json(li.field_confidence)
                    else:
                        st.info("No confidence data available.")

            except ValidationError as ve:
                st.error(" Schema validation failed.")
                st.text(str(ve))

            except Exception as e:
                st.error(" Extraction failed.")
                st.text(str(e))

st.divider()
st.caption("Built as a PRD-based AI Prototype for Inquiry Structuring • Core Intelligence Layer")

