from django.shortcuts import render, redirect, get_object_or_404
from .models import Skill, Experience, Project,Folder, FolderImage
from .forms import FolderForm,CustomUserCreationForm
from .serializers import FolderSerializer
from rest_framework import viewsets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

def home(request):
    return render(request, 'home.html', {
        'skills': Skill.objects.all(),
        'experiences': Experience.objects.all().order_by('-start_date'),
        'projects': Project.objects.all(),
    })


# Lista y creación
def folder_list(request):
    form = FolderForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            folder = form.save()
            # aquí guardas todas las imágenes subidas
            for f in request.FILES.getlist('images'):
                FolderImage.objects.create(folder=folder, image=f)
            return redirect('folder_list')
        # si no es válido, caerá al final y mostrará los errores
    folders = Folder.objects.prefetch_related('images').order_by('-created_at')
    return render(request, 'folder_list.html', {'form': form, 'folders': folders})

# Edición
def folder_edit(request, pk):
    folder = get_object_or_404(Folder, pk=pk)
    form = FolderForm(request.POST or None, request.FILES or None, instance=folder)
    if form.is_valid():
        folder = form.save()
        for file in request.FILES.getlist('images'):
            FolderImage.objects.create(folder=folder, image=file)
        return redirect('folder_list')
    return render(request, 'folder_edit.html', {'form': form, 'folder': folder})

# Eliminación
def folder_delete(request, pk):
    folder = get_object_or_404(Folder, pk=pk)
    if request.method == 'POST':
        folder.delete()
        return redirect('folder_list')
    return render(request, 'folder_delete.html', {'folder': folder})


class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.order_by('-created_at')
    serializer_class = FolderSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)


# Registro de usuario
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('welcome')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def welcome(request):
    # Contador de visitas por sesión
    visits = request.session.get('visits', 0) + 1
    request.session['visits'] = visits
    # Total de usuarios registrados
    from django.contrib.auth.models import User
    total_users = User.objects.count()
    return render(request, 'auth/welcome.html', {
        'visits': visits,
        'total_users': total_users,
    })

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']
    next_page = 'home'

    def get(self, request, *args, **kwargs):
        # Llama al post para procesar logout en GET
        return self.post(request, *args, **kwargs)
    
