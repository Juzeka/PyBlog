from django.shortcuts import render, redirect

from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q,Count,Case,When
from comentario.forms import ComentarioForm
from comentario.models import Comentario
from django.contrib import messages


# Create your views here.

class PostIndex(ListView):
    model = Post
    template_name = 'post/index.html'
    paginate_by = 6
    context_object_name = 'posts' #nome do objeto para chamar no Template


    def get_queryset(self):
        qs = super().get_queryset() # chamando o get_queryset padrao e adicionando mais coisas
        qs = qs.order_by('-id').filter(publicado_post=True) #ordem decrecente pelo id e filtrando por post publicado
        qs = qs.select_related('categoria_post')
        qs = qs.annotate(        #contar
            numero_comentarios = Count(
                #caso
                Case(
                    #quando nome da chave primaria(FK)_nome do campo tem que ser True pra contar(THEN) 1
                    When(comentario__publicado_comentario = True, then=1)
                )
            )
        )

        return qs

class PostBusca(PostIndex):
    template_name = 'post/post_busca.html'

    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.get('termo')

        if not termo:
            return qs

        qs = qs.filter(# icontains = não diferencia maiusculo de minusculo
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo) #quando o campo for do tipo Foregen Key tem que usar IEXACT
        )

        return qs




class PostCategoria(PostIndex):
    template_name = 'post/post_categoria.html' #caminho do template

    def get_queryset(self):
        qs = super().get_queryset()# Herança - chamando o get_queryset padrao já adicionado mais codigos lá em PostIndex e adicionando mais coisas
        categoria = self.kwargs.get('categoria', None)# verifica qual paramentro está sendo passado no kwargs

        if not categoria:
            return qs
                      #campo do model FK+__+nome do campo que queres utilizar+__+tipo da pesquisa requerida
        qs = qs.filter(categoria_post__nome_cat__iexact = categoria)# iexact = quer um valor igual mais so que em case sensitive
        return qs

class PostDetalhe(UpdateView):
    template_name = 'post/post_detalhe.html'
    model = Post
    form_class = ComentarioForm
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        post = self.get_object()
        comentarios = Comentario.objects.filter(publicado_comentario= True, post_comentario= post.id).order_by('-id')

        contexto['comentarios'] = comentarios



        return contexto

    def form_valid(self, form):
        post = self.get_object()
        comentario = Comentario(**form.cleaned_data)
        comentario.post_comentario = post

        if self.request.user.is_authenticated:
            comentario.usuario_comentario = self.request.user

        comentario.save()
        messages.success(self.request, 'Comentário enviado com sucesso!')
        return redirect('post_detalhe',pk = post.id)