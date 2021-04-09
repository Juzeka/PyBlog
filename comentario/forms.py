from django.forms import  ModelForm
from .models import Comentario

class ComentarioForm(ModelForm):
    def clean(self):
        data = self.cleaned_data

        nome = data.get('nome_comentario')
        email = data.get('email_comentario')
        comentario = data.get('comentario_comentario')

        if len(nome)<5:
            self.add_error(
                'nome_comentario','O nome precisa ter mais de 5 caracteres!'
            )

        if not comentario:
            self.add_error(
                #nome do campo            mensagem para exibição
                'comentario_comentario', 'Faça um comentario'
            )

    class Meta:
        model = Comentario
        fields = ('nome_comentario','email_comentario','comentario_comentario')