from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # LOGIN PADRÃO DO DJANGO
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('relatorio/', views.relatorio, name='relatorio'),
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('gestao/', views.dashboard_gestao, name='dashboard_gestao'),
    path('painel/', views.painel_admin, name='painel_admin'),
]