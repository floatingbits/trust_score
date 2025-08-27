from django.contrib.auth.models import Group, User
from trust_score.api.models import ReviewPage, Review
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'text', 'rated_date', 'author_name', 'created']


class ReviewPageSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = ReviewPage
        fields = ['id', 'url', 'title', 'created', 'reviews']
