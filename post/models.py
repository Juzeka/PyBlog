from django.db import models
from categoria.models import Categoria
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    titulo_post = models.CharField(max_length=50, verbose_name= 'Título')
    autor_post = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name= 'Autor')
    data_post = models.DateTimeField(auto_now_add=True, verbose_name= 'Data')
    conteudo_post = models.TextField(verbose_name= 'Conteudo')
    excerto_post = models.TextField(verbose_name= 'Excerto')
    categoria_post = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name= 'Categoria')
    image_post = models.ImageField(upload_to='post_img/%Y/%m/%d', blank=True, null=True, verbose_name= 'Imagem')
    publicado_post = models.BooleanField(default=False, verbose_name= 'Publicado')


    def __str__(self):
        return self.titulo_post + ' ' + str(self.autor_post)