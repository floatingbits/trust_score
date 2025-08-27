
PROMPT_DEFAULT = """
Du bist ein Analysesystem für Online-Bewertungen. 
Dir liegt eine Sammlung von Bewertungen zu einer Weiterbildungseinrichtung vor. 
Jede Bewertung hat den eigentlichen Text und eine Sternenzahl (1–5). 
Bitte analysiere jede Bewertung und gib Bewertungen in den folgenden Kategorien (0–1) zurück:

Kategorien:
1. depth_of_content: Ist der Text konkret, mit spezifischen Details, Fachbegriffen oder Beispielen, 
   oder ist er generisch und floskelhaft?
2. balance: Wirkt der Text ausgewogen mit positiven und negativen Aspekten, oder ist er nur einseitig euphorisch oder kritisch?
4. product_vs_sales: 0 = Fokus stark auf Vertrieb oder Verkaufsberatung, 1 = Fokus stark auf Lerninhalte/Qualität der Weiterbildung.
5. authenticity: Wie authentisch wirkt der Text im Ausdruck? 0 = sehr werblich/übertrieben/floskelhaft, 1 = natürlicher Erfahrungsbericht.



Wichtig:
- Gib ausschließlich ein JSON-Array zurück, wobei jedes Element eine Bewertung repräsentiert.

Beispiel-Ausgabeformat:
[
  {{
    "review_id": "1",
    "depth_of_content": 0.35,
    "balance": 0.10,
    "product_vs_sales": 0.15,
    "authenticity": 0.40
  }},
  {{
    "review_id": "2",
    "depth_of_content": 0.70,
    "balance": 0.40,
    ...
  }}
]

---

Hier sind die Bewertungen (jede mit ID, Sternenzahl und Text):

{reviews}

"""

REVIEW_TEMPLATE_DEFAULT = "{consecutive_number}. [ID={review_id}, Sterne={rating}] \"{text}\""


class PromptGenerator:
    def __init__(self, template: str):
        self.template = template

    def generate(self, reviews):
        review_texts = "\n".join([
            REVIEW_TEMPLATE_DEFAULT.format(
                consecutive_number=index,
                text=r.text,
                review_id=r.id,
                rating=r.rating
            ) for index, r in enumerate(reviews)
        ])
        return self.template.format(reviews=review_texts)
