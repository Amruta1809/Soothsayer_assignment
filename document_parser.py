import pdfplumber
import pandas as pd

import fitz  # PyMuPDF

def parse_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text, []

def parse_excel(file):
    dataframes = pd.read_excel(file, sheet_name=None)  # Read all sheets
    return dataframes

def extract_financial_metrics(text, tables):
    """
    Very simple keyword-based extraction.
    In real apps you’d add NLP or regex rules.
    """
    metrics = {}
    keywords = ["Revenue", "Total Revenue", "Sales", "Expenses", "Net Income", "Profit"]

    for kw in keywords:
        if kw.lower() in text.lower():
            # Naive search - you can extend with regex
            idx = text.lower().find(kw.lower())
            snippet = text[idx:idx+50]
            metrics[kw] = snippet
    
    return metrics

