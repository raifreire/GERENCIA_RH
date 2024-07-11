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

    colaborador_list = Colaborador.objects.all().filter(user=request.user)
    contador = Colaborador.objects.count()
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
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            colaborador = form.save(commit=False)
            colaborador.user = request.user
            colaborador.save()
            return redirect(reverse('colaborador-lista'))
    else:
        form = ColaboradorForm()

    return render(request, 'main/form_colaborador.html', {'form': form})

class ColaboradorUpdateView(UpdateView):
    '''
    Função para atualizar os colaboradores'''
    model = Colaborador
    form_class = ColaboradorForm
    template_name = 'main/form_colaborador.html'
    success_url = reverse_lazy('colaborador-lista')

def deleteColaborador(request, id):
    '''
    Função para deletar os colaboradores'''
    colaborador = get_object_or_404(Colaborador, pk=id)
    colaborador.delete()
    return redirect('/')


# def filtro(request, classificacao):
#     colaborador_list = Colaborador.objects.filter(classificacao=classificacao)
#     return render(request, 'main/colaborador.html',{'colaboradores_list': colaborador_list})

def buscar(request):
    # if not request.user.is_authenticated:
    #     messages.error(request, 'Usuário não logado')
    #     return redirect('login')

    colaborador_list = Colaborador.objects.all()
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            colaborador_list = colaborador_list.filter(nome__icontains=nome_a_buscar)
            return render(request, "main/colaborador.html", {"colaboradores_list": colaborador_list})
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
        colaborador_list = Colaborador.objects.all()

        departamento_selecionado = request.POST.get('departamento')
        classificacao_selecionada = request.POST.get('classificacao')
        
        if departamento_selecionado == '' and classificacao_selecionada == '':
            contador = Colaborador.objects.count()
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
            print(contrato)
            return redirect(reverse('colaborador-lista'))
    else:
        form = ContratoForm()

    return render(request, 'main/form_contrato.html', {'form': form})

def contrato_view(request ):
    '''Função para listar os contratos'''
    contratos = Contrato.objects.all()
    return render(request,'main/contrato.html',{'contratos':contratos})


#TODO:preciso exibir nos detalhes do colaborador os contratos associados a ele
#TODO:preciso filtrar os contratos por nome do colaborador dentro da pagina contrato
#TODO:criar aba desligados com data da saida e filtros
#TODO: data de encerramento do contrato na pag contratos

def contrato_view_for_name(request, name):
    '''
    Função para detalhar os contratos pelo nome do colaborador'''
    contratos = Contrato.objects.filter(colaborador__nome=name)
    return render(request,'main/contrato.html',{'contratos':contratos})