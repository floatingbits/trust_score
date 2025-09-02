import datetime
import re

from trustpilot_scraper.scraper import scrape_trustpilot_reviews
from trust_score.api.domain.repository import ReviewPageRepository, ReviewRepository
from trust_score.api.domain.entities import Review as ReviewEntity, ReviewPage as ReviewPageEntity


class ReviewPageService:
    def fetch_and_store_reviews(self, review_page: ReviewPageEntity):
        repo = ReviewRepository()
        reviews_json = self.get_reviews_from_page(review_page.url)
        for review_json in reviews_json:
            # print(review_json)
            emoji_pattern = re.compile("["
                                       u"\U0001F600-\U0001F64F"  # emoticons
                                       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                       u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                       "]+", flags=re.UNICODE)

            text = self.remove_emojis(review_json.get("Body"))
            repo.create(
                author_name=review_json.get("Author"),
                text=text,
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

    def remove_emojis(self, data):
        emoj = re.compile("["
                          u"\U0001F600-\U0001F64F"  # emoticons
                          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                          u"\U0001F680-\U0001F6FF"  # transport & map symbols
                          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          u"\U00002500-\U00002BEF"  # chinese char
                          u"\U00002702-\U000027B0"
                          u"\U000024C2-\U0001F251"
                          u"\U0001f926-\U0001f937"
                          u"\U00010000-\U0010ffff"
                          u"\u2640-\u2642"
                          u"\u2600-\u2B55"
                          u"\u200d"
                          u"\u23cf"
                          u"\u23e9"
                          u"\u231a"
                          u"\ufe0f"  # dingbats
                          u"\u3030"
                          "]+", re.UNICODE)
        return re.sub(emoj, '', data)
