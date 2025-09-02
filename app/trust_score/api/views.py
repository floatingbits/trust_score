import os

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from django.db.models import Model

from trust_score.api.serializers import GroupSerializer, UserSerializer, ReviewPageSerializer, ReviewSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from trust_score.api.models import ReviewPage
from trust_score.api.services.review_page_service import ReviewPageService
from trust_score.api.domain.repository import ReviewPageRepository
from trust_score.api.clients.gpt_client import GptClient

from trust_score.api.services.trust_rating_training_service import TrustRatingTrainingDataService

from trust_score.api.services.prompt_generator import PROMPT_DEFAULT, PromptGenerator

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET', 'POST'])
def review_page_list(request):
    """
    List all review pages, or create a new review_page.
    """
    if request.method == 'GET':
        reviews = ReviewPage.objects.all()
        serializer = ReviewPageSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewPageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def review_page_detail(request, pk):
    """
    List all review pages, or create a new review_page.
    """
    try:
        review_page = ReviewPage.objects.get(pk=pk)
        serializer = ReviewPageSerializer(review_page)
        return Response(serializer.data)
    except ReviewPage.objects.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def review_page_scrape(request, pk):
    """
    List all review pages, or create a new review_page.
    """
    try:
        repo = ReviewPageRepository()
        review_page = repo.get(pk)
        review_page_service = ReviewPageService()
        review_page_service.fetch_and_store_reviews(review_page)
        review_page_model = ReviewPage.objects.get(pk=pk)
        serializer = ReviewPageSerializer(review_page_model)
        return Response(serializer.data)
    except ReviewPage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def review_page_generate_training_data(request, pk):
    """
    List all review pages, or create a new review_page.
    """
    try:
        client = GptClient(os.environ.get("OPENAI_API_KEY"), "gpt-4.1")
        prompt_generator = PromptGenerator(PROMPT_DEFAULT)
        service = TrustRatingTrainingDataService(prompt_generator, client)
        service.generate_trust_rating_training(pk)
        return Response([])
    except ReviewPage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)