from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Usuario(AbstractUser):
    is_psicologo = models.BooleanField(default=False)
    telefone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    foto_perfil = models.ImageField(upload_to="usuarios/", blank=True, null=True)

    def __str__(self):
        return self.username


class Postagem(models.Model):
    autor = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="postagens"
    )
    conteudo = models.TextField()
    criado_em = models.DateTimeField(default=timezone.now)
    anonima = models.BooleanField(default=False)

    def __str__(self):
        return f"Postagem {self.id} - {'Anônimo' if self.anonima else self.autor.username}"


class Comentario(models.Model):
    postagem = models.ForeignKey(
        Postagem, on_delete=models.CASCADE, related_name="comentarios"
    )
    autor = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="comentarios"
    )
    conteudo = models.TextField()
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comentário {self.id} de {self.autor.username}"


class Curtida(models.Model):
    postagem = models.ForeignKey(
        Postagem, on_delete=models.CASCADE, related_name="curtidas"
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="curtidas"
    )
    criado_em = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["postagem", "usuario"], name="unique_curtida"
            )
        ]

    def __str__(self):
        return f"{self.usuario.username} curtiu Postagem {self.postagem.id}"


class Denuncia(models.Model):
    TIPO_CHOICES = [
        ("postagem", "Postagem"),
        ("comentario", "Comentário"),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    postagem = models.ForeignKey(
        Postagem, on_delete=models.CASCADE, null=True, blank=True, related_name="denuncias"
    )
    comentario = models.ForeignKey(
        Comentario, on_delete=models.CASCADE, null=True, blank=True, related_name="denuncias"
    )
    usuario_denunciante = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="denuncias"
    )
    motivo = models.TextField()
    criado_em = models.DateTimeField(default=timezone.now)
    resolvido = models.BooleanField(default=False)

    def __str__(self):
        return f"Denúncia de {self.usuario_denunciante.username} ({self.tipo})"


class Consulta(models.Model):
    paciente = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="consultas_paciente"
    )
    psicologo = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="consultas_psicologo"
    )
    data_hora = models.DateTimeField()
    criado_em = models.DateTimeField(default=timezone.now)
    confirmado = models.BooleanField(default=False)
    cancelado = models.BooleanField(default=False)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return f"Consulta {self.id} - {self.paciente.username} com {self.psicologo.username}"
