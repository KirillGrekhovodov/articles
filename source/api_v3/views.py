from django.db.models import Count
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api_v2.serializers import ArticleModelSerializer
from webapp.models import Article


# Create your views here.

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer

    # permission_classes = [DjangoModelPermissions]
    #
    # throttle_classes = []
    def perform_create(self, serializer):
        author = self.request.user
        print(author)
        serializer.save(author=author)

    def get_permissions(self):
        super().get_permissions()
        if self.request.method in SAFE_METHODS:
            return []
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        return Response({"test": "test"})

    def retrieve(self, request, *args, **kwargs):
        print(self.get_object())
        return Response(ArticleModelSerializer(self.get_object()).data)

    def get_serializer_class(self):
        print(self.action, "!!!!")
        if self.action in ("retrieve", "list"):
            # if self.request.method == "GET":
            return ArticleModelSerializer
        return ArticleModelSerializer

    # http://localhost:8000/api/v3/articles/get_comments_count
    @action(methods=["GET"], detail=True, url_path="comments-count")
    def get_comments_count(self, request, *args, **kwargs):
        article = self.get_object()
        return Response({"comments_count": article.comments.count()})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user.auth_token.delete()
        return Response({'status': 'ok'})
