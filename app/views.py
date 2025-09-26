from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Usuario  # seu modelo personalizado

# Página inicial = login
def index(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")  # página após login
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "index.html")


# Página de cadastro
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm = request.POST["confirm"]

        if password != confirm:
            messages.error(request, "As senhas não coincidem!")
            return redirect("register")

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "Usuário já existe!")
            return redirect("register")

        # criar usuário usando seu modelo
        user = Usuario(username=username)
        user.set_password(password)  # criptografa a senha
        user.save()

        messages.success(request, "Conta criada com sucesso! Faça login.")
        return redirect("index")

    return render(request, "register.html")


# Logout
def logout_view(request):
    logout(request)
    return redirect("index")


# Página principal após login
def home(request):
    return render(request, "home.html", {"user": request.user})
