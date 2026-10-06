# Duplicate Customer Detector

A Python-based application for identifying potential duplicate customer records using data normalization, exact matching, blocking, similarity scoring, and human review.

## Project Objective

The application identifies potential duplicate customer records based on:

- Customer name
- Email
- Phone number
- Address

The system flags potential duplicates for human review instead of automatically deleting or merging customer records.

## Technology Stack

- Python
- Pandas
- Streamlit
- RapidFuzz
- CSV

## Detection Pipeline

Customer Data
↓
Normalization
↓
Remove Punctuation
↓
Exact Matching
↓
First-Letter Blocking
↓
Similarity Scoring
↓
Threshold Evaluation
↓
Duplicate Flagging
↓
Human Review
↓
Final Output

## How to Run

```bash
pip install -r requirements.txt

```text
streamlit run app.py