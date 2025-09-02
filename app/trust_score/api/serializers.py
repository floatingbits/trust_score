from django.contrib.auth.models import Group, User
from trust_score.api.models import ReviewPage, Review, TrustScore
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TrustScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrustScore
        fields = ['id', 'result_json', 'rating_algorithm_key', 'rating_model_key', 'rating_model_priority']


class ReviewSerializer(serializers.ModelSerializer):
    trust_scores = TrustScoreSerializer(many=True, read_only=True)
    class Meta:
        model = Review
        fields = ['rating', 'text', 'rated_date', 'author_name', 'created', 'trust_scores']


class ReviewPageSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = ReviewPage
        fields = ['id', 'url', 'title', 'created', 'reviews']
