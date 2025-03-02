from django.urls import path
from . import views

urlpatterns = [
    path('', views.colaboradorView, name='colaborador-lista'),
    path('colaboradorID/<int:id>', views.colaboradorIDview, name='colaborador-detalhe'),
    path('colaborador/create/', views.adicionar_colaborador_view, name='colaborador-create'),
    path('colaborador/<int:pk>/update/', views.atualizar_colaborador_view, name='colaborador-update'),
    path('delete/<int:id>', views.deletar_colaborador_view, name="delete-colaborador"),
    path('colaboradores_por_departamento', views.colaboradores_por_departamento_view, name="colaboradores_por_departamento"),
    path('contrato/create/', views.adicionar_contrato_view, name='contrato-create'),
    path('contrato/', views.contrato_view, name='contrato'),
    path('contratoID/<int:id>', views.contrato_id_view, name='contrato-detalhe'),
    path('contrato/<int:pk>/update/', views.atualizar_contrato_view, name='contrato_update'),
    path('contrato_view_for_name/<str:name>', views.contrato_por_nome_view, name='contrato_view_name'),
    path('buscar', views.buscar, name='buscar'),
    path('desligados/', views.colaborador_desligado_view, name='colaborador-desligado'),
]
