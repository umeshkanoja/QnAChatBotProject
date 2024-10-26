from django.db import models
from django.contrib.auth.models import User
from pgvector.django import VectorField, HnswIndex

# Create your models here.

class File(models.Model):
    file = models.FileField(upload_to="files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="files")
        
    def __str__(self):
        return self.file.name

class Embedding(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="embeddings")
    embedding = VectorField(
        dimensions=1536,
        blank=True,
        null=True,
        help_text="The embedding of the file, generated by a OpenAI model"
    )

    class Meta:
        indexes = [
            HnswIndex(
                name="embedding_index",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"]
            )
        ]

    def __str__(self):
        return self.file.file.name