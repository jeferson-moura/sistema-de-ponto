from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count
import openpyxl
from django.shortcuts import render, redirect
from .models import RegistroPonto
from django.contrib import messages

from django.contrib.auth.decorators import login_required
# verifica se é administrador
def is_admin(user):
    return user.is_superuser


@login_required
def dashboard(request):

    if request.method == "POST":
        tipo = request.POST.get("tipo")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        hoje = now().date()

        # Bloquear entrada duplicada
        if tipo == "entrada":
            entrada_existente = RegistroPonto.objects.filter(
                funcionario=request.user,
                tipo="entrada",
                data_hora__date=hoje
            ).exists()

            if entrada_existente:
                messages.warning(request, "Entrada já registrada hoje.")
                return redirect("dashboard")

        atrasado = False

        if tipo == "entrada":
            hora_atual = now().time()
            hora_limite = settings.HORA_LIMITE_ENTRADA

            if hora_atual > hora_limite:
                atrasado = True
                messages.warning(request, "Entrada registrada com atraso.")
            else:
                messages.success(request, "Entrada registrada com sucesso.")

        elif tipo == "almoco_saida":
            messages.info(request, "Saída para almoço registrada.")

        elif tipo == "almoco_volta":
            messages.info(request, "Volta do almoço registrada.")

        elif tipo == "saida":
            messages.success(request, "Saída registrada com sucesso.")

        RegistroPonto.objects.create(
            funcionario=request.user,
            tipo=tipo,
            latitude=latitude,
            longitude=longitude,
            atrasado=atrasado
        )

        return redirect("dashboard")

    # últimos registros
    registros = RegistroPonto.objects.filter(
        funcionario=request.user
    ).order_by("-data_hora")[:10]

    # STATUS DO DIA
    hoje = now().date()

    registros_hoje = RegistroPonto.objects.filter(
        funcionario=request.user,
        data_hora__date=hoje
    ).order_by("data_hora")

    status = "Nenhum ponto registrado hoje"

    if registros_hoje.exists():
        ultimo = registros_hoje.last().tipo

        if ultimo == "entrada":
            status = "Entrada registrada"
        elif ultimo == "almoco_saida":
            status = "Em horário de almoço"
        elif ultimo == "almoco_volta":
            status = "Trabalhando após almoço"
        elif ultimo == "saida":
            status = "Expediente finalizado"

    return render(request, "ponto/dashboard.html", {
        "registros": registros,
        "status": status
    })


# RELATÓRIO ADMIN
@user_passes_test(is_admin)
def relatorio(request):
    registros = RegistroPonto.objects.all().order_by("-data_hora")

    return render(request, "ponto/relatorio.html", {
        "registros": registros
    })


# EXPORTAR EXCEL
@user_passes_test(is_admin)
def exportar_excel(request):

    registros = RegistroPonto.objects.all().order_by("-data_hora")

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Relatório de Ponto"

    sheet.append([
        "Funcionário",
        "Data",
        "Hora",
        "Tipo",
        "Atraso"
    ])

    for r in registros:
        sheet.append([
            r.funcionario.username,
            r.data_hora.strftime("%d/%m/%Y"),
            r.data_hora.strftime("%H:%M"),
            r.tipo,
            "Sim" if r.atrasado else "Não"
        ])

    response = HttpResponse(
        content_type="application/ms-excel"
    )
    response["Content-Disposition"] = "attachment; filename=relatorio_ponto.xlsx"

    workbook.save(response)

    return response


# DASHBOARD DE GESTÃO
@user_passes_test(is_admin)
def dashboard_gestao(request):

    hoje = now().date()

    funcionarios = User.objects.count()

    pontos_hoje = RegistroPonto.objects.filter(
        data_hora__date=hoje
    ).count()

    atrasos_hoje = RegistroPonto.objects.filter(
        data_hora__date=hoje,
        atrasado=True
    ).count()

    ranking = RegistroPonto.objects.values(
        "funcionario__username"
    ).annotate(
        total=Count("id")
    ).order_by("-total")[:5]

    context = {
        "funcionarios": funcionarios,
        "pontos_hoje": pontos_hoje,
        "atrasos_hoje": atrasos_hoje,
        "ranking": ranking,
    }

    return render(request, "ponto/dashboard_gestao.html", context)

@user_passes_test(is_admin)
def painel_admin(request):
    return redirect("/admin/")
