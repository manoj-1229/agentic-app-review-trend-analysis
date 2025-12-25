# Agentic AI – App Review Trend Analysis

This project implements an agentic AI system that analyzes Google Play
Store reviews, consolidates similar feedback, and tracks issue trends
from T-30 to T.

## Agentic Architecture
1. Data Ingestion Agent – Daily review batches
2. Topic Extraction Agent – Extracts issues and requests
3. Deduplication Agent – Merges semantically similar topics
4. Trend Aggregation Agent – Builds trend table

## How to Run
```bash
pip install pandas
python agentic_review_trend_final.py
