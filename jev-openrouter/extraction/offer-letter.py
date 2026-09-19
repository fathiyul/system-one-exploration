import os
import re

import requests
from dotenv import load_dotenv


load_dotenv()

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

text = """
Dear Alex,

We are pleased to offer you the position of Senior Machine Learning Engineer
at Acme Technologies.

Your annual base salary will be $180,000. You will also receive a one-time
signing bonus of $15,000 and an equity award representing 0.25% of the
company's fully diluted shares.

Your anticipated start date is October 15, 2026. You will report directly
to Sarah Elizabeth Johnson, Director of Artificial Intelligence.

Sincerely,
Daniel Roberts
Chief People Officer
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
    "percent": re.compile(
        r"\b(?:100(?:\.0+)?|\d{1,2}(?:\.\d+)?)\s?%"
    ),
    "name": re.compile(
        r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}\b"
    ),
    "title": re.compile(
        r"\b(?:"
        r"(?:Junior|Senior|Lead|Principal|Staff|Chief|Associate|Assistant|"
        r"Director|Head|VP|Vice President)?\s*"
        r"(?:[A-Z][A-Za-z/&-]*\s+){0,4}"
        r"(?:Engineer|Scientist|Analyst|Developer|Manager|Designer|"
        r"Architect|Consultant|Researcher|Officer|Director|Specialist)"
        r")\b"
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
        "id": "job_title",
        "kind": "title",
        "question": "new hire's job title",
    },
    {
        "id": "base_salary",
        "kind": "money",
        "question": "annual base salary being offered",
    },
    {
        "id": "start_date",
        "kind": "date",
        "question": "anticipated start date",
    },
    {
        "id": "equity",
        "kind": "percent",
        "question": (
            "equity award as a percentage of fully diluted shares"
        ),
    },
    {
        "id": "manager_name",
        "kind": "name",
        "question": "name of the person the new hire reports to",
    },
    {
        "id": "signing_bonus",
        "kind": "money",
        "question": "one-time signing bonus amount",
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

for field in fields:
    answer = answers[field["id"]]

    print(
        f"{field['id']}:",
        answer["choice"],
        f"(confidence: {answer['confidence']:.2f})",
    )
