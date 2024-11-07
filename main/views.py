from .models import Colaborador, Contrato
from .forms import ColaboradorForm, ContratoForm
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

@login_required #define que o usuario esteja logado, para ter acesso as informações. Deve-se colocar em todas as funcões privadas.
def colaboradorView(request):
    '''
    Função para listar os colaboradores
    '''
    if not request.user.is_authenticated:
        return redirect('login')
   
    colaborador_list = Colaborador.objects.all().filter(user=request.user).filter(ativo_inativo=True)
    contador = Colaborador.objects.filter(ativo_inativo=True).count()
    return render(request, 'main/colaborador.html', {'colaboradores_list': colaborador_list,'quantidade':contador})


def colaboradorIDview(request, id):
    '''
    Função para detalhar os colaboradores pelo ID'''
    colaborador = get_object_or_404(Colaborador, pk=id)
    return render(request, 'main/colaboradorID.html', {'colaborador': colaborador})


@login_required
def colaborador_create_view(request):
    '''
    Função para criar os colaboradores'''
    if request.method == 'POST':
        form = ColaboradorForm(request.POST,request.FILES)
        if form.is_valid():
            colaborador = form.save(commit=False)
            colaborador.user = request.user
            colaborador.save()
            return redirect(reverse('colaborador-lista'))
    else:
        form = ColaboradorForm()

    return render(request, 'main/form_colaborador.html', {'form': form})


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
            colaborador_list = colaboradores.filter(nome__icontains=nome_a_buscar)
            return render(request, "main/colaborador.html", {"colaboradores_list": colaborador_list})
        else:
            return render(request, 'main/contrato.html')  
    
    if "buscar_desligados" in request.GET:
        nome_a_buscar = request.GET['buscar_desligados']
        if nome_a_buscar:
            colaboradores_desligados = Colaborador.objects.filter(ativo_inativo=False)
            colaboradores_desligados_list = colaboradores_desligados.filter(nome__icontains=nome_a_buscar)
            print(colaboradores_desligados)
            return render(request, "main/colaborador_desligado.html", {"colaboradores_list": colaboradores_desligados_list})
        else:
            return render(request, 'main/contrato.html')
        
    if "buscar_contrato" in request.GET:
        nome_a_buscar = request.GET['buscar_contrato']
        if nome_a_buscar:
            """para conseguir me referenciar ao nome do colaborador utilizei o 
            nome do campo foreign key em contrato + 'underscore undescore' e o
            nome do campo do Colaborador."""
            contratos = Contrato.objects.filter(colaborador__nome__icontains=nome_a_buscar)
            return render(request,'main/contrato.html',{'contratos':contratos})
    else:
        return render(request, 'main/contrato.html')    


def filtrar_colaborador(request):
    if request.method == 'POST':
        # colaborador_list = Colaborador.objects.all()
        colaborador_list = Colaborador.objects.filter(ativo_inativo=True)
        contador = colaborador_list.count()

        departamento_selecionado = request.POST.get('departamento')
        classificacao_selecionada = request.POST.get('classificacao') # funcionario/estagiario/mei
        data_inicial = request.POST.get('data_inicial')
        data_final = request.POST.get('data_final')

        if data_inicial and data_final:
            colaborador_list_for_data = colaborador_list.filter(data_entrada__range=[data_inicial, data_final])
            contador_for_data = colaborador_list_for_data.count()
            return render(request, 'main/filtros.html', {'colaboradores_list':colaborador_list_for_data,'quantidade':contador_for_data})

        if departamento_selecionado == '' and classificacao_selecionada == '':
            return render(request, 'main/filtros.html', {'colaboradores_list':colaborador_list,'quantidade':contador})
        if departamento_selecionado != '':
            colaborador_filtrado_departamento = colaborador_list.filter(departamento=departamento_selecionado)
            if classificacao_selecionada == '':
                contador = len(colaborador_filtrado_departamento)
                return render(request, 'main/filtros.html', {'colaboradores_list':colaborador_filtrado_departamento,'quantidade':contador})
        if classificacao_selecionada != '':
            if departamento_selecionado == '':
                colaborador_filtrado_classificacao = colaborador_list.filter(classificacao=classificacao_selecionada)
                contador=len(colaborador_filtrado_classificacao)
                return render(request, 'main/filtros.html', {'colaboradores_list':colaborador_filtrado_classificacao,'quantidade':contador})    
            else:
                colaborador_filtrado_classificacao = colaborador_filtrado_departamento.filter(classificacao=classificacao_selecionada)
                contador = len(colaborador_filtrado_classificacao)
                return render(request, 'main/filtros.html', {'colaboradores_list':colaborador_filtrado_classificacao,'quantidade':contador})    
    else:
        return render(request, 'main/filtros.html')
    

def contrato_create_view(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST,request.FILES)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.user = request.user
            contrato.save()
            contrato=request.FILES.get('contrato')
            return redirect(reverse('colaborador-lista'))
    else:
        form = ContratoForm()

    return render(request, 'main/form_contrato.html', {'form': form})


def contrato_view(request ):
    '''Função para listar os contratos'''
    contratos = Contrato.objects.all()
    return render(request,'main/contrato.html',{'contratos':contratos})


def contrato_view_for_name(request, name):
    '''
    Função para detalhar os contratos pelo nome do colaborador'''
    contratos = Contrato.objects.filter(colaborador__nome=name)
    return render(request,'main/contrato.html',{'contratos':contratos})


def colaborador_desligado_view(request):
    '''Função para listar os colaboradores desligados'''
    if request.method == 'GET':
        colaboradores = Colaborador.objects.filter(ativo_inativo=False)
        contador = colaboradores.count()
        return render(request,'main/colaborador_desligado.html',{'colaboradores_list':colaboradores, 'quantidade':contador})
    if request.method == 'POST':
        colaboradores = Colaborador.objects.filter(ativo_inativo=False)

        data_inicial = request.POST.get('data_inicial')
        data_final = request.POST.get('data_final')

        if data_inicial and data_final:
            colaborador_list = colaboradores.filter(data_saida__range=[data_inicial, data_final])
            contador = colaborador_list.count()
            return render(request, 'main/colaborador_desligado.html', {'colaboradores_list':colaborador_list,'quantidade':contador})

        contador = Colaborador.objects.filter(ativo_inativo=False).count()
        return render(request,'main/colaborador_desligado.html',{'colaboradores_list':colaboradores, 'quantidade':contador})


######################## TO DO ####################################################
#TODO: criar relatorios de ferias, renovacao.
# usar timedelta para somatorio de datas?
######################## TO DO ####################################################
