# services/teacher_rating_service.py
from trust_score.api.models import Review, TrustRating
from trust_score.api.services.prompt_generator import PromptGenerator
from trust_score.api.clients.gpt_client import GptClient
from django.db import transaction


class TrustRatingTrainingService:
    def __init__(self, prompt_generator: PromptGenerator, gpt_client: GptClient):
        self.prompt_generator = prompt_generator
        self.gpt_client = gpt_client

    @transaction.atomic
    def generate_trust_rating_training(self, review_page_id: int):
        reviews = Review.objects.filter(review_page_id=review_page_id)
        prompt = self.prompt_generator.generate(reviews)
        result = self.gpt_client.run_prompt(prompt)

        TrustRating.objects.create(
            review_page_id=review_page_id,
            result=result
        )
        return result
