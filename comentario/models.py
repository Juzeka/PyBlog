from django.db import models
from post.models import Post
from django.contrib.auth.models import User

# Create your models here.
class Comentario(models.Model):
    nome_comentario = models.CharField(max_length=50, blank=False, null=False, verbose_name= 'Nome')
    email_comentario = models.EmailField(verbose_name= 'Email')
    comentario_comentario = models.TextField(verbose_name= 'Comentário')
    post_comentario = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name= 'Post')
    usuario_comentario = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name= 'Usuário', blank=True, null=True)
    data_comentario = models.DateTimeField(auto_now_add=True, verbose_name= 'Data')
    publicado_comentario = models.BooleanField(default=False, verbose_name= 'Publicado')


    def __str__(self):
        return self.nome_comentario