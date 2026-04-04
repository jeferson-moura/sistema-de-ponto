from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 👇 TODAS as rotas do sistema vêm daqui
    path('', include('ponto.urls')),
]