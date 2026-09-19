import os
import re

import requests
from dotenv import load_dotenv


load_dotenv()

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

text = """
MASTER SERVICES AGREEMENT
Agreement No. REF-MSA-2026-0412

This Master Services Agreement (the "Agreement") is entered into as of October 1, 2026 (the "Effective Date") between Bright Harbor Systems, Inc., a Delaware corporation with offices at 1400 Waterline Avenue, Suite 900, Wilmington, DE 19801 ("Client"), and Kestrel Data Works LLC, a Colorado limited liability company with offices at 77 Mesa Ridge Road, Boulder, CO 80302 ("Provider"). The parties signed this Agreement on September 24, 2026. It replaces the prior consulting agreement REF-MSA-2024-0103 dated March 15, 2024, which ran for three years and is terminated as of the Effective Date without further obligation on either side.

1. Services. Provider will deliver the data platform engineering services described in Statement of Work SO-2026-0412-01 (the "SOW") and in any later statement of work the parties sign under this Agreement. Work under the SOW begins on October 6, 2026. Provider's quote QUO-2026-0388 dated August 29, 2026 is superseded in full by this Agreement and the SOW. Client will issue purchase order PO-88210 to cover the first twelve invoices, and Provider must reference it on every invoice it sends.

2. Term and renewal. The initial term of this Agreement is 24 months from the Effective Date (the "Initial Term"). After the Initial Term the Agreement renews automatically for successive 12 month periods (each a "Renewal Term") unless either party gives written notice of non-renewal at least ninety days before the end of the then-current term. A statement of work that is still in progress when the Agreement ends continues under these terms until it is complete or terminated.

3. Fees. Client will pay Provider a fixed fee of $18,500.00 per month for the services in the SOW, invoiced monthly in advance beginning November 1, 2026. A one-time onboarding fee of $12,000.00 is due with the first invoice. Work outside the SOW is billed at $215.00 per hour and requires Client's prior written approval. Reasonable travel is reimbursed at cost up to $3,000.00 per calendar quarter. Fees under the prior agreement were $16,200.00 per month and do not carry forward. On each anniversary of the Effective Date the monthly fee may increase by no more than 3%.

4. Payment. Invoices are payable within 45 days of receipt. Client may dispute an invoice in good faith within 10 business days of receipt, and undisputed amounts remain due on schedule. Late amounts accrue interest at 1.5% per month or the maximum rate permitted by law, whichever is lower. Billing questions go to ap@brightharborsystems.com and invoices are sent to billing@brightharborsystems.com. Provider's finance contact is Priya Raman, and Client's finance contact is Devon Marsh.

5. Service levels. Provider will maintain 99.9% monthly availability for the managed pipelines described in the SOW, measured as set out there. If availability falls below 99.9% in any month, Client receives a service credit of 10% of that month's fee, and if it falls below 99.0% the credit is 25%. Provider will acknowledge priority incidents within 4 hours and all other requests within 5 business days. Support requests are tracked as tickets, and the open migration ticket TKT-4471 is carried over from the prior engagement.

6. Personnel. Provider's engagement lead is Amara Okonkwo, Principal Engineer, and its account manager is Noah Castellanos. Provider may replace personnel with people of equal qualification after notifying Client in writing. Client's project sponsor is Devon Marsh, Director of Operations, who approves deliverables on Client's behalf.

7. Confidentiality. Each party will protect the other's Confidential Information with at least the care it uses for its own, and no less than reasonable care, for five years after disclosure. Trade secrets remain protected for as long as they qualify as trade secrets. Confidential Information does not include information that is public through no fault of the receiving party or that the receiving party already held without restriction.

8. Intellectual property. Deliverables identified as such in the SOW are works made for hire and belong to Client on payment. Provider retains its pre-existing tools, libraries and know-how and grants Client a perpetual, royalty-free license to use them as embedded in the deliverables.

9. Warranties. Provider warrants that the services will be performed in a professional and workmanlike manner by qualified people. Client must report a breach of this warranty within 30 days of delivery, and Provider will re-perform the affected services or refund the fees paid for them. This is Client's sole remedy for breach of warranty.

10. Limitation of liability. Except for breaches of confidentiality, indemnity obligations and Client's obligation to pay fees, neither party's aggregate liability under this Agreement will exceed $222,000.00, which is the total of the fees payable in the twelve months before the claim. Neither party is liable for indirect, incidental or consequential damages, including lost profits, even if advised of their possibility.

11. Termination. Either party may terminate this Agreement for convenience on 120 days written notice. Either party may terminate for material breach if the breach is not cured within 30 days of written notice describing it. On termination Provider will return or delete Client data within 60 days, and Client will pay for services performed through the termination date. No early termination fee applies.

12. Notices. Legal notices must be in writing and sent to Client at legal@brightharborsystems.com, attention Grant Whitlock, General Counsel, with a copy by courier to the address above, and to Provider at contracts@kestreldataworks.com, attention Tobias Reinholt. Operational communications may go to amara.okonkwo@kestreldataworks.com or support@kestreldataworks.com. Notices are effective on receipt.

13. Governing law. This Agreement is governed by the laws of the State of Delaware without regard to its conflict of laws rules, and the parties submit to the state and federal courts located in New Castle County, Delaware.

14. Entire agreement. This Agreement, with its statements of work, is the entire agreement between the parties on its subject and supersedes all earlier agreements, proposals and quotes. It may be amended only in a writing signed by both parties.

Signed for Bright Harbor Systems, Inc. by Helena Vasquez, Chief Operating Officer, on September 24, 2026.
Signed for Kestrel Data Works LLC by Tobias Reinholt, Managing Member, on September 23, 2026.
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
        r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|"
        r"ten|eleven|twelve|thirty|sixty|ninety)\s+"
        r"(?:calendar\s+|business\s+)?"
        r"(?:hour|hours|day|days|week|weeks|month|months|year|years)"
        r"\b",
        re.IGNORECASE,
    ),
    "percent": re.compile(
        r"\b(?:100(?:\.0+)?|\d{1,2}(?:\.\d+)?)\s?%"
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
        "id": "agreement_number",
        "kind": "id",
        "question": (
            "number of this agreement—not the prior agreement, "
            "SOW, quote, PO, or ticket"
        ),
    },
    {
        "id": "effective_date",
        "kind": "date",
        "question": (
            "effective date of this agreement—not the signing "
            "date or SOW start"
        ),
    },
    {
        "id": "initial_term",
        "kind": "duration",
        "question": "length of the initial term",
    },
    {
        "id": "renewal_term",
        "kind": "duration",
        "question": "length of each automatic renewal period",
    },
    {
        "id": "termination_notice",
        "kind": "duration",
        "question": (
            "notice period to terminate for convenience—not "
            "non-renewal or cure"
        ),
    },
    {
        "id": "payment_terms",
        "kind": "duration",
        "question": "time allowed to pay an invoice after receipt",
    },
    {
        "id": "monthly_fee",
        "kind": "money",
        "question": (
            "fixed monthly fee under this agreement—not the prior "
            "fee, onboarding fee, or hourly rate"
        ),
    },
    {
        "id": "liability_cap",
        "kind": "money",
        "question": "cap on either party's aggregate liability",
    },
    {
        "id": "late_interest",
        "kind": "percent",
        "question": "monthly interest rate on late payments",
    },
    {
        "id": "uptime",
        "kind": "percent",
        "question": (
            "monthly availability Provider commits to—not a "
            "credit or fee increase"
        ),
    },
    {
        "id": "client_signatory",
        "kind": "name",
        "question": (
            "person who signed for the Client, "
            "Bright Harbor Systems"
        ),
    },
    {
        "id": "notices_email",
        "kind": "email",
        "question": "email address for legal notices to the Client",
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
