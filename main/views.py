from .models import Colaborador, Contrato
from .forms import ColaboradorForm, ContratoForm
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse, reverse_lazy
from rolepermissions.decorators import has_role_decorator


def colaboradorView(request):
    '''
    Função para listar os colaboradores
    '''
    if not request.user.is_authenticated:
        return redirect('login')    
    if request.method == 'GET':
        colaboradores = Colaborador.objects.filter(ativo_inativo=True)
        contador = colaboradores.count()
        user = request.user.username
        return render(request, 'main/colaborador.html', {'colaboradores_list': colaboradores, 'quantidade': contador, 'username': user})
    if request.method == 'POST':
        colaborador_list = Colaborador.objects.filter(ativo_inativo=True)
        contador = colaborador_list.count()

        departamento_selecionado = request.POST.get('departamento')
        classificacao_selecionada = request.POST.get('classificacao')  # funcionario/estagiario/mei
        data_inicial = request.POST.get('data_inicial')
        data_final = request.POST.get('data_final')

        if data_inicial and data_final:
            colaborador_list_for_data = colaborador_list.filter(
                data_entrada__range=[data_inicial, data_final])
            contador_for_data = colaborador_list_for_data.count()
            return render(request, 'main/colaborador.html', {'colaboradores_list': colaborador_list_for_data, 'quantidade': contador_for_data})

        if departamento_selecionado == '' and classificacao_selecionada == '':
            return render(request, 'main/colaborador.html', {'colaboradores_list': colaborador_list, 'quantidade': contador})
        if departamento_selecionado != '':
            colaborador_filtrado_departamento = colaborador_list.filter(
                departamento=departamento_selecionado)
            if classificacao_selecionada == '':
                contador = len(colaborador_filtrado_departamento)
                return render(request, 'main/colaborador.html', {'colaboradores_list': colaborador_filtrado_departamento, 'quantidade': contador})
        if classificacao_selecionada != '':
            if departamento_selecionado == '':
                colaborador_filtrado_classificacao = colaborador_list.filter(
                    classificacao=classificacao_selecionada)
                contador = len(colaborador_filtrado_classificacao)
                return render(request, 'main/colaborador.html', {'colaboradores_list': colaborador_filtrado_classificacao, 'quantidade': contador})
            else:
                colaborador_filtrado_classificacao = colaborador_filtrado_departamento.filter(
                    classificacao=classificacao_selecionada)
                contador = len(colaborador_filtrado_classificacao)
                return render(request, 'main/colaborador.html', {'colaboradores_list': colaborador_filtrado_classificacao, 'quantidade': contador})
    else:
        return render(request, 'main/colaborador.html')


def colaboradorIDview(request, id):
    '''
    Função para detalhar os colaboradores pelo ID'''
    colaborador = get_object_or_404(Colaborador, pk=id)
    return render(request, 'main/colaboradorID.html', {'colaborador': colaborador})


@has_role_decorator('admin')
def colaborador_create_view(request):
    '''
    Função para criar os colaboradores'''
    if request.method == 'POST':
        form = ColaboradorForm(request.POST, request.FILES)
        if form.is_valid():
            colaborador = form.save(commit=False)
            colaborador.user = request.user
            colaborador.save()
            return redirect(reverse('colaborador-lista'))
    else:
        form = ColaboradorForm()

    return render(request, 'main/form_colaborador.html', {'form': form})


@has_role_decorator('admin')
def colaboradorUpdateView(request, pk):
    colaborador = get_object_or_404(Colaborador, pk=pk)
    if request.method == "POST":
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            colaborador = form.save(commit=False)
            if colaborador.data_saida:
                colaborador.ativo_inativo = False
            colaborador.save()
            return redirect(reverse_lazy('colaborador-lista'))
    else:
        form = ColaboradorForm(instance=colaborador)

    return render(request, 'main/form_colaborador.html', {'form': form})


@has_role_decorator('admin')
def deleteColaborador(request, id):
    '''
    Função para deletar os colaboradores'''
    colaborador = get_object_or_404(Colaborador, pk=id)
    colaborador.delete()
    return redirect('/')


def buscar(request):
    colaborador_list = Colaborador.objects.all()

    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            colaboradores = Colaborador.objects.filter(ativo_inativo=True)
            colaborador_list = colaboradores.filter(
                nome__icontains=nome_a_buscar)
            return render(request, "main/colaborador.html", {"colaboradores_list": colaborador_list})
        else:
            return render(request, 'main/colaborador.html')

    if "buscar_desligados" in request.GET:
        nome_a_buscar = request.GET['buscar_desligados']
        if nome_a_buscar:
            colaboradores_desligados = Colaborador.objects.filter(
                ativo_inativo=False)
            colaboradores_desligados_list = colaboradores_desligados.filter(
                nome__icontains=nome_a_buscar)
            print(colaboradores_desligados)
            return render(request, "main/colaborador_desligado.html", {"colaboradores_list": colaboradores_desligados_list})
        else:
            return render(request, 'main/colaborador_desligado.html')

    if "buscar_contrato" in request.GET:
        nome_a_buscar = request.GET['buscar_contrato']
        if nome_a_buscar:
            """para conseguir me referenciar ao nome do colaborador utilizei o 
            nome do campo foreign key em contrato + 'underscore undescore' e o
            nome do campo do Colaborador."""
            contratos = Contrato.objects.filter(
                colaborador__nome__icontains=nome_a_buscar)
            return render(request, 'main/contrato.html', {'contratos': contratos})
    else:
        return render(request, 'main/contrato.html')


@has_role_decorator('admin')
def contrato_create_view(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST, request.FILES)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.user = request.user
            contrato.save()
            return redirect(reverse('colaborador-lista'))
    else:
        form = ContratoForm()
        
    return render(request, 'main/form_contrato.html', {'form': form})


@has_role_decorator('admin')
def contrato_update_view(request, pk):
    if request.method == 'GET':
        contrato = get_object_or_404(Contrato, pk=pk)
        form = ContratoForm(instance=contrato)
        return render(request, 'main/form_contrato.html', {'form': form})
    if request.method == 'POST':
        contrato = get_object_or_404(Contrato, pk=pk)
        form = ContratoForm(request.POST, request.FILES, instance=contrato)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.user = request.user
            contrato.save()
            contrato = request.FILES.get('contrato')
            return redirect('colaborador-lista')
    else:
        form = ContratoForm()
    return render(request, 'main/form_contrato.html', {'form': form})


def contrato_view(request):
    '''Função para listar os contratos'''
    if request.method=="GET":
        contratos = Contrato.objects.all()
        return render(request, 'main/contrato.html', {'contratos': contratos})

    if request.method == 'POST':
        contrato_list = Contrato.objects.all()
        contador = contrato_list.count()

        periodo_selecionado = request.POST.get('periodo')  # funcionario/estagiario/mei
        data_inicial = request.POST.get('data_inicial')
        data_final = request.POST.get('data_final')

        if data_inicial and data_final:
            contrato_list_for_data = contrato_list.filter(
                data_inicio__range=[data_inicial, data_final])
            contador_for_data = contrato_list_for_data.count()
            return render(request, 'main/contrato.html', {'contratos': contrato_list_for_data, 'quantidade': contador_for_data})

        if periodo_selecionado == '':
            return render(request, 'main/contrato.html', {'contratos': contrato_list, 'quantidade': contador})
        
        if periodo_selecionado != '':
            contrato_filtrado_periodo = contrato_list.filter(periodo=periodo_selecionado)
            return render(request, 'main/contrato.html', {'contratos': contrato_filtrado_periodo, 'quantidade': contrato_filtrado_periodo.count()})
        
    else:
        return render(request, 'main/contrato.html')


def contrato_id_view(request, id):
    '''
    Função para detalhar os contratos pelo ID'''
    contrato = get_object_or_404(Contrato, pk=id)
    return render(request, 'main/contratoID.html', {'contrato': contrato})


def contrato_view_for_name(request, name):
    '''
    Função para detalhar os contratos pelo nome do colaborador'''
    contratos = Contrato.objects.filter(colaborador__nome=name)
    return render(request, 'main/contrato.html', {'contratos': contratos})


def colaborador_desligado_view(request):
    '''Função para listar os colaboradores desligados'''
    if request.method == 'GET':
        colaboradores = Colaborador.objects.filter(ativo_inativo=False)
        contador = colaboradores.count()
        return render(request, 'main/colaborador_desligado.html', {'colaboradores_list': colaboradores, 'quantidade': contador})
    if request.method == 'POST':
        colaborador_list = Colaborador.objects.filter(ativo_inativo=False)
        contador = colaborador_list.count()

        departamento_selecionado = request.POST.get('departamento_desligado')
        classificacao_selecionada = request.POST.get('classificacao_desligado')  # funcionario/estagiario/mei
        data_inicial = request.POST.get('data_inicial_desligado')
        data_final = request.POST.get('data_final_desligado')

        if data_inicial and data_final:
            colaborador_list_for_data = colaborador_list.filter(
                data_entrada__range=[data_inicial, data_final])
            contador_for_data = colaborador_list_for_data.count()
            return render(request, 'main/colaborador_desligado.html', {'colaboradores_list': colaborador_list_for_data, 'quantidade': contador_for_data})

        if departamento_selecionado == '' and classificacao_selecionada == '':
            return render(request, 'main/colaborador_desligado.html', {'colaboradores_list': colaborador_list, 'quantidade': contador})
        if departamento_selecionado != '':
            colaborador_filtrado_departamento = colaborador_list.filter(
                departamento=departamento_selecionado)
            if classificacao_selecionada == '':
                contador = len(colaborador_filtrado_departamento)
                return render(request, 'main/colaborador_desligado.html', {'colaboradores_list': colaborador_filtrado_departamento, 'quantidade': contador})
        if classificacao_selecionada != '':
            if departamento_selecionado == '':
                colaborador_filtrado_classificacao = colaborador_list.filter(
                    classificacao=classificacao_selecionada)
                contador = len(colaborador_filtrado_classificacao)
                return render(request, 'main/colaborador_desligado.html', {'colaboradores_list': colaborador_filtrado_classificacao, 'quantidade': contador})
            else:
                colaborador_filtrado_classificacao = colaborador_filtrado_departamento.filter(
                    classificacao=classificacao_selecionada)
                contador = len(colaborador_filtrado_classificacao)
                return render(request, 'main/colaborador_desligado.html', {'colaboradores_list': colaborador_filtrado_classificacao, 'quantidade': contador})
    else:
        return render(request, 'main/colaborador_desligado.html')


######################## TO DO ####################################################
# TODO: criar relatorios de ferias, renovacao.
# usar timedelta para somatorio de datas?
######################## TO DO ####################################################
