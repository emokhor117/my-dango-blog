from django.shortcuts import render
from .serializers import PostSerializer
from post.models import Post
from rest_framework import viewsets, permissions

# Create your views here.
# CRUD

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)