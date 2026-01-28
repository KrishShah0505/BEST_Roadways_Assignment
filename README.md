# AI Inquiry Inbox — PRD Prototype

This project is a working prototype of the core intelligence layer of an enterprise system that converts unstructured logistics inquiry emails into structured RFQ records.

It is based on the provided Product Requirements Document (PRD) for the "AI Inquiry Ingestion & Structuring System". The goal of this implementation is to demonstrate how the most critical and complex part of the system — understanding unstructured emails and converting them into structured data — can be designed and built.

This is not a full production system. It is a focused, engineering-driven MVP that implements the brain of the pipeline.

---

## What This Project Does

The system takes a raw email (free text) and:

- Classifies whether it is an inquiry or not
- Extracts structured data using an LLM with a fixed schema
- Supports multiple lanes (multiple shipments in one email)
- Normalizes key fields such as vehicle types and city names
- Assigns confidence scores to critical fields
- Decides whether the inquiry requires human review
- Presents the result in a simple Streamlit interface

The output is a structured JSON object that matches the schema described in the PRD.

---

## System Architecture

The system is designed as a deterministic pipeline around an LLM:

Input Email
↓
Rule-based Inquiry Classifier
↓
LLM-based Schema-constrained Extraction (Groq)
↓
JSON Validation (Pydantic)
↓
Normalization Layer (Vehicle Types, Cities)
↓
Confidence Scoring and Review Decision
↓
Final Structured Output


A key design principle is that the LLM is used only for extraction. All validation, normalization, confidence scoring, and review decisioning are handled using deterministic code to ensure reliability and auditability.

---

## What Is In Scope

- Inquiry vs non-inquiry classification
- Schema-locked structured extraction using an LLM
- Multi-lane support
- Field normalization
- Confidence scoring per field
- Needs-review decisioning
- A Streamlit UI for demonstration

---

## What Is Out of Scope

- Gmail ingestion
- Dashboard backend and workflows
- User management
- Deduplication and threading
- Training pipelines

These are integration and scale layers that would sit around this core intelligence module in a full system.

---

## How to Run

1. Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt


Set your Groq API key in a .env file:

GROQ_API_KEY=your_key_here


Run the application:

streamlit run app.py

Project Structure
ai-inquiry-parser/
├── app.py
├── extractor.py
├── schema.py
├── classifier.py
├── normalizer.py
├── validator.py
├── data/
│   └── sample_emails/
└── README.md

Design Rationale

This project follows a production-style design approach:

The LLM is treated as an unreliable component and is constrained strictly to extraction

All business rules, validation, confidence scoring, and review logic are deterministic

This ensures that the system is debuggable, auditable, and safe for real business use

The architecture mirrors how such a system would be built in a real enterprise environment

How This Maps to the Original PRD

This prototype implements the core parts of:

Inquiry Detection

Unstructured Extraction

Schema-locked Output

Normalization

Confidence Scoring and Human-in-the-loop decisioning

The remaining parts of the PRD (Gmail ingestion, dashboard, workflows, monitoring) are system integration layers that would be built around this core.

Limitations

The extraction quality depends on the LLM

The normalization dictionaries are minimal and illustrative

Date parsing and location resolution are basic and not production-grade

This is a functional prototype, not a production system



