from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (
    home,
    folder_list,
    folder_edit,
    folder_delete,
    FolderViewSet,
    register,
    welcome,
    contacto,
    CustomLogoutView,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api/folders', FolderViewSet, basename='api-folders')

urlpatterns = [
    path('', home, name='home'),
    path('folders/', folder_list, name='folder_list'),
    path('folders/<int:pk>/edit/', folder_edit, name='folder_edit'),
    path('folders/<int:pk>/delete/', folder_delete, name='folder_delete'),

    # Autenticación de usuarios
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('welcome/', welcome, name='welcome'),
    path('contact/', contacto, name='contact')
]

urlpatterns += router.urls