from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('relatorio/', views.relatorio, name='relatorio'),
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('gestao/', views.dashboard_gestao, name='dashboard_gestao'),
    path('painel/', views.painel_admin, name='painel_admin'),
]