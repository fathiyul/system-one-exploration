import os
import re

import requests
from dotenv import load_dotenv


load_dotenv()

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

text = """
Invoice INV-2026-1042

Total due: $1,250.00
Payment due date: October 15, 2026
Purchase order: PO-A91XZ
Billing questions: billing@example.com
"""


finders = {
    "money": re.compile(
        r"[$€£]\s?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?"
    ),
    "id": re.compile(
        r"\b(?:INV|PO|REF|ORD|SO|CN|ACC|CASE|TKT|QUO)-"
        r"[A-Z0-9][A-Z0-9-]*\b"
    ),
    "email": re.compile(
        r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"
    ),
    "date": re.compile(
        r"\b(?:"
        r"\d{4}[-/]\d{1,2}[-/]\d{1,2}"
        r"|"
        r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}"
        r"|"
        r"(?:January|February|March|April|May|June|July|August|"
        r"September|October|November|December)"
        r"\s+\d{1,2},?\s+\d{4}"
        r")\b",
        re.IGNORECASE,
    ),
}


def candidates(text: str, kind: str) -> list[str]:
    """Return unique matches in their original document order."""
    matches = (
        match.group(0).strip()
        for match in finders[kind].finditer(text)
    )
    return list(dict.fromkeys(matches))


fields = [
    {
        "id": "invoice_number",
        "kind": "id",
        "question": "invoice number of the new invoice being sent",
    },
    {
        "id": "total_due",
        "kind": "money",
        "question": "total amount due on the new invoice",
    },
    {
        "id": "due_date",
        "kind": "date",
        "question": "payment due date of the new invoice",
    },
    {
        "id": "po_number",
        "kind": "id",
        "question": "purchase order reference for the new invoice",
    },
    {
        "id": "billing_email",
        "kind": "email",
        "question": "email address for billing questions",
    },
]


questions = {}

for field in fields:
    field_candidates = candidates(text, field["kind"])

    criteria = {
        value: "This exact value as it appears in the document."
        for value in field_candidates
    }
    criteria["none"] = "No candidate in the document is this value."

    questions[field["id"]] = {
        "type": "choice",
        "instructions": f"Which candidate is the {field['question']}?",
        "criteria": criteria,
    }


response = requests.post(
    url="https://openrouter.ai/api/alpha/decisions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "typesafe/jev-1.13",
        "state": {
            "description": (
                "A document to extract fields from. "
                "Judge only from `document`."
            ),
            "document": text,
        },
        "questions": questions,
    },
    timeout=60,
)

response.raise_for_status()

answers = response.json()["answers"]

invoice_number = answers["invoice_number"]["choice"]
invoice_confidence = answers["invoice_number"]["confidence"]

print("Invoice number:", invoice_number)
print("Confidence:", invoice_confidence)
