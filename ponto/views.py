from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User

from .models import RegistroPonto


# 🔥 CRIA ADMIN AUTOMÁTICO
def criar_admin_automatico():
    if not User.objects.filter(username='ana_cristina').exists():
        User.objects.create_superuser(
            username='ana_cristina',
            password='ana883314',
            email=''
        )

# 🟢 DASHBOARD (TELA PRINCIPAL)
@login_required
def dashboard(request):
    # 👇 AQUI É O LOCAL CORRETO
    criar_admin_automatico()
    User.objects.filter(username='ana_cristina').delete()

    criar_admin_automatico()
    agora = timezone.now()
    hoje = agora.date()

    registro = RegistroPonto.objects.filter(
        funcionario=request.user,
        data=hoje
    ).first()

    context = {
        'hora_atual': agora,
        'registro': registro
    }

    return render(request, 'dashboard.html', context)


# 🟢 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# 🟢 RELATÓRIO
@login_required
def relatorio(request):
    registros = RegistroPonto.objects.filter(funcionario=request.user)
    return render(request, 'relatorio.html', {'registros': registros})


# 🟢 EXPORTAR EXCEL
@login_required
def exportar_excel(request):
    import openpyxl
    from django.http import HttpResponse

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Relatório de Ponto"

    ws.append(['Data', 'Entrada', 'Saída'])

    registros = RegistroPonto.objects.filter(funcionario=request.user)

    for r in registros:
        ws.append([
            str(r.data),
            str(r.entrada),
            str(r.saida),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=relatorio.xlsx'

    wb.save(response)
    return response


# 🟢 DASHBOARD DE GESTÃO
@login_required
def dashboard_gestao(request):
    total = RegistroPonto.objects.count()
    return render(request, 'gestao.html', {'total': total})


# 🟢 PAINEL ADMIN SIMPLES
@login_required
def painel_admin(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    usuarios = User.objects.all()
    return render(request, 'painel.html', {'usuarios': usuarios})