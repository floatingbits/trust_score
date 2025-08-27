import datetime

from trust_score.api.models import ReviewPage as ReviewPageModel, Review as ReviewModel
from trust_score.api.domain.entities import ReviewPage as ReviewPageEntity, Review as ReviewEntity


class ReviewPageRepository:
    def create(self, title, url) -> ReviewPageEntity:
        review_page_model = ReviewPageModel.objects.create(title=title, url=url)

        return ReviewPageEntity(
            id=review_page_model.id,
            title=review_page_model.title,
            url=review_page_model.url,
            created=review_page_model.created
        )

    def get(self, review_page_id) -> ReviewPageEntity:
        review_page_model = ReviewPageModel.objects.get(id=review_page_id)
        return ReviewPageEntity(
            id=review_page_model.id,
            title=review_page_model.title,
            url=review_page_model.url,
            created=review_page_model.created
        )


class ReviewRepository:
    def create(self, author_name: str, text: str, rating: int, rated_date: datetime.datetime, review_page: ReviewPageEntity) -> ReviewEntity:
        review_model = ReviewModel.objects.create(
            author_name=author_name, text=text, review_page_id=review_page.id, rating=rating, rated_date=rated_date
        )

        return ReviewEntity(
            id=review_model.id,
            author_name=review_model.author_name,
            text=review_model.text,
            created=review_model.created,
            rated_date=review_model.rated_date,
            rating=review_model.rating,
            review_page=review_page
        )

    def get_all_for_review_page(self, review_page_id: int) -> list[ReviewEntity]:
        review_models = ReviewModel.objects.filter(review_page_id=review_page_id)
        return review_models

