from django.contrib import admin

# Register your models here.
from .models import Usuario, Postagem, Comentario, Curtida, Denuncia, Consulta

admin.site.register(Usuario)
admin.site.register(Postagem)
admin.site.register(Comentario)
admin.site.register(Curtida)
admin.site.register(Denuncia)
admin.site.register(Consulta)
