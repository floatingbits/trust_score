from datasets import Dataset
from .entities import TrustScore


ALGORITHM_KEY_DEFAULT_CATEGORIES = "default_categories"


class MultiLabelConverter:
    def convert_to_multi_label(self, trust_score: TrustScore):

        match trust_score.rating_algorithm_key:
            case _:
                label_names = self.get_label_names(trust_score.rating_algorithm_key)
                result = []
                for label_name in label_names:
                    result.append(trust_score.result_json.get(label_name))
                return result

    def get_label_names(self, rating_algorithm_key):
        global ALGORITHM_KEY_DEFAULT_CATEGORIES
        match rating_algorithm_key:
            case ALGORITHM_KEY_DEFAULT_CATEGORIES:
                return [
                    "depth_of_content",
                    "balance",
                    "product_vs_sales",
                    "authenticity"
                ]

class DatasetConverter:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def convert_to_dataset(self, trust_scores: list[TrustScore]) -> Dataset:

        # -------------------------------
        # 1. Beispiel-Daten
        # -------------------------------
        # texts = [
        #     "Die Beratung war sehr oberflächlich.",
        #     "Sehr freundliche und detaillierte Erklärung, top!",
        #     "Alles super, aber ein bisschen zu kurz gefasst.",
        #     "Die Dozentin half mir, die Optionen zu priorisieren."
        # ]
        #
        # # Labels: [Tiefe, Balance, Stil]  (Skala 0.0–1.0)
        # labels = [
        #     [0.1, 0.4, 0.6],
        #     [0.9, 0.8, 0.9],
        #     [0.5, 0.3, 0.7],
        #     [0.8, 0.7, 0.8]
        # ]

        texts = []
        labels = []
        multilabel_converter = MultiLabelConverter()
        for trust_score in trust_scores:
            texts.append(trust_score.review.text)
            current_multi_labels = multilabel_converter.convert_to_multi_label(trust_score)
            labels.append(current_multi_labels)

        dataset = Dataset.from_dict({"text": texts, "label": labels})

        def tokenize(batch):
            return self.tokenizer(batch["text"], padding=True, truncation=True)

        return dataset.map(tokenize, batched=True)
