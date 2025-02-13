from django.shortcuts import render

# Create your views here.
from rest_framework import generics ,status
from rest_framework.response import Response

from .models import BlogPost
from .serializer import BlogPostSerializer
from rest_framework.views import APIView

class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def delete(self, request, *args, **kwargs):
        BlogPost.objects.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlogPostupdate(generics.RetrieveUpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'pk'


class BlogPostList(APIView):
    def get(self, request, format=None):
        title= request.query_params.get('title')

        if title:
            BlogPost = BlogPost.objects.filter(title__icontains=title)
        else:
            BlogPost=  BlogPost.objects.all()

        serializer = BlogPostSerializer(BlogPost, many=True)
        return Response(serializer.data ,status=status.HTTP_200_OK)