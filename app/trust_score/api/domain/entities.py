import datetime
from dataclasses import dataclass


@dataclass
class ReviewPage:
    id: int | None
    created: datetime.datetime
    title: str
    url: str


@dataclass
class Review:
    id: int | None
    created: datetime.datetime
    author_name: str
    text: str
    review_page: ReviewPage
    rating: int
    rated_date: datetime.datetime



