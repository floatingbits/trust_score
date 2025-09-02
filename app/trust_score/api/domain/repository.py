import datetime

from trust_score.api.models import ReviewPage as ReviewPageModel, Review as ReviewModel, TrustScore as TrustScoreModel
from trust_score.api.domain.entities import ReviewPage as ReviewPageEntity, Review as ReviewEntity, \
    TrustScore as TrustScoreEntity


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

    @staticmethod
    def instantiate_from_model(review_page_model: ReviewPageModel):
        return ReviewPageEntity(
            id=review_page_model.id,
            title=review_page_model.title,
            url=review_page_model.url,
            created=review_page_model.created
        )


class ReviewRepository:
    def create(self, author_name: str, text: str, rating: int, rated_date: datetime.datetime,
               review_page: ReviewPageEntity) -> ReviewEntity:
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

    def get(self, review_id) -> ReviewEntity:
        review_model = ReviewModel.objects.get(id=review_id)
        return self.instantiate_from_model(review_model)

    @staticmethod
    def instantiate_from_model(review_model: ReviewModel) -> ReviewEntity:
        review_page = ReviewPageRepository.instantiate_from_model(review_model.review_page)
        return ReviewEntity(
            id=review_model.id,
            author_name=review_model.author_name,
            text=review_model.text,
            created=review_model.created,
            rated_date=review_model.rated_date,
            rating=review_model.rating,
            review_page=review_page
        )


    # def get_all_for_review_page(self, review_page_id: int) -> list[ReviewEntity]:
    #     review_models = ReviewModel.objects.filter(review_page_id=review_page_id)
    #     return review_models


class TrustScoreRepository:
    def create(self, author_name: str, text: str, rating: int, rated_date: datetime.datetime,
               review_page: ReviewPageEntity) -> TrustScoreEntity:
        trust_score_model = TrustScoreModel.objects.create(
            author_name=author_name, text=text, review_page_id=review_page.id, rating=rating, rated_date=rated_date
        )

        return self.instantiate_from_model(trust_score_model)

    @staticmethod
    def instantiate_from_model(model: TrustScoreModel):
        return TrustScoreEntity(
            id=model.id,
            created=model.created,
            result_json=model.result_json,
            rating_algorithm_key=model.rating_algorithm_key,
            rating_model_key=model.rating_model_key,
            rating_model_priority=model.rating_model_priority,
            review=ReviewRepository.instantiate_from_model(model.review)
        )

    @staticmethod
    def get_all() -> list[TrustScoreEntity]:
        trust_score_models = TrustScoreModel.objects.all()
        result = []
        for model in trust_score_models:
            result.append(TrustScoreRepository.instantiate_from_model(model))

        return result
