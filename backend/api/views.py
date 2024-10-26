from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from .models import File, Embedding
from .serializers import FileSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.utils.embedding_utils import generate_embedding, get_split_text
from api.utils.openai_utils import get_openai_response
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
    
class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            # Get the file from the serializer
            file = serializer.instance.file
            # Generate the embedding
            split_text = get_split_text(file)
            for text in split_text:
                embedding_instance = Embedding(
                    text=text,
                    file=serializer.instance,
                    author=self.request.user,
                    embedding=generate_embedding(text)
                )
                embedding_instance.save()
        else:
            print(serializer.errors)
        
    def perform_destroy(self, instance):
        instance.delete()


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_query(request):
    question = request.data.get('q')
    
    result = {
        "answer": get_openai_response(request.user, question)
    }
    response = Response(result)
    return response
