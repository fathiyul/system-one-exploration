import os
import re

import requests
from dotenv import load_dotenv


load_dotenv()

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

text = """
Residential Lease Agreement

This lease is between landlord Sarah Elizabeth Johnson and tenant
Michael Brown.

The lease begins on October 1, 2026. It was signed on September 15, 2026.

The monthly rent is $1,500.00.
The security deposit is $3,000.00.
A separate pet deposit of $500.00 is required.

The tenant must provide 30 days' notice to end the tenancy.
The landlord must provide 24 hours' notice before entering the property.
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
    "duration": re.compile(
        r"\b\d+\s+"
        r"(?:hour|hours|day|days|week|weeks|month|months|year|years)"
        r"(?:['’]?\s+notice)?\b",
        re.IGNORECASE,
    ),
    "name": re.compile(
        r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}\b"
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
        "id": "monthly_rent",
        "kind": "money",
        "question": "monthly rent amount",
    },
    {
        "id": "security_deposit",
        "kind": "money",
        "question": (
            "security deposit—not the pet deposit or late fee"
        ),
    },
    {
        "id": "lease_start",
        "kind": "date",
        "question": "lease start date—not the signing date",
    },
    {
        "id": "notice_period",
        "kind": "duration",
        "question": (
            "notice period to end the tenancy—not entry notice"
        ),
    },
    {
        "id": "landlord_name",
        "kind": "name",
        "question": "landlord's full name",
    },
]


questions = {}

for field in fields:
    field_candidates = candidates(text, field["kind"])

    criteria = {
        value: "This exact value as it appears in the document."
        for value in field_candidates
    }
    criteria["none"] = (
        "No candidate in the document is this value."
    )

    questions[field["id"]] = {
        "type": "choice",
        "instructions": (
            f"Which candidate is the {field['question']}?"
        ),
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

print(
    "Monthly rent:",
    answers["monthly_rent"]["choice"],
    answers["monthly_rent"]["confidence"],
)

print(
    "Security deposit:",
    answers["security_deposit"]["choice"],
    answers["security_deposit"]["confidence"],
)

print(
    "Lease start:",
    answers["lease_start"]["choice"],
    answers["lease_start"]["confidence"],
)

print(
    "Notice period:",
    answers["notice_period"]["choice"],
    answers["notice_period"]["confidence"],
)

print(
    "Landlord:",
    answers["landlord_name"]["choice"],
    answers["landlord_name"]["confidence"],
)
