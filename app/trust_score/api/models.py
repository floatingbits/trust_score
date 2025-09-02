from django.db import models


# Create your models here.
class ReviewPage(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    url = models.CharField(max_length=256, blank=True, default='')

    objects = models.Manager()

    class Meta:
        ordering = ['created']


class Review(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, default='')
    author_name = models.CharField(max_length=255, blank=True, default='')
    rating = models.IntegerField()
    rated_date = models.DateTimeField(auto_now_add=False)
    review_page = models.ForeignKey(ReviewPage, related_name='reviews', on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        ordering = ['created']


class TrustScore(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    result_json = models.JSONField()
    rating_algorithm_key = models.CharField(max_length=50)
    rating_model_key = models.CharField(max_length=50)
    rating_model_priority = models.IntegerField()

    review = models.ForeignKey(Review, related_name='trust_scores', on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        ordering = ['created']
        unique_together = (("rating_algorithm_key", "rating_model_key", "review"),)
