from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.models import User


def criar_admin_automatico():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='ana_cristina',
            password='ana883314',
            email=''
        )
urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # LOGIN PADRÃO DO DJANGO
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('relatorio/', views.relatorio, name='relatorio'),
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('gestao/', views.dashboard_gestao, name='dashboard_gestao'),
    path('painel/', views.painel_admin, name='painel_admin'),
]