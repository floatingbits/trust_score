import datetime

from trustpilot_scraper.scraper import scrape_trustpilot_reviews
from trust_score.api.domain.repository import ReviewPageRepository, ReviewRepository
from trust_score.api.domain.entities import Review as ReviewEntity, ReviewPage as ReviewPageEntity


class ReviewPageService:
    def fetch_and_store_reviews(self, review_page: ReviewPageEntity):
        repo = ReviewRepository()
        reviews_json = self.get_reviews_from_page(review_page.url)
        for review_json in reviews_json:
            # print(review_json)
            repo.create(
                author_name=review_json.get("Author"),
                text=review_json.get("Body"),
                review_page=review_page,
                rating=review_json.get("Rating"),
                rated_date=datetime.datetime.strptime(review_json.get("Date"), "%Y-%m-%d")
            )

    def create_review_page(self, base_url: str) -> ReviewPageEntity:
        repo = ReviewPageRepository()
        title = base_url
        review_page = repo.create(title=title, url=base_url)
        self.fetch_and_store_reviews(review_page)
        return review_page

    def get_reviews_from_page(self, base_url: str):
        return scrape_trustpilot_reviews(base_url)
