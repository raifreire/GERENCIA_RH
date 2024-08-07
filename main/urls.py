from django.urls import path
from . import views

urlpatterns = [
    path('', views.colaboradorView, name='colaborador-lista'),
    path('desligados/', views.colaborador_desligado_view, name='colaborador-desligado'),
    path('colaboradorID/<int:id>', views.colaboradorIDview, name='colaborador-detalhe'),
    path('colaborador/create/', views.colaborador_create_view, name='colaborador-create'),
    path('contrato/create/', views.contrato_create_view, name='contrato-create'),
    path('contrato/', views.contrato_view, name='contrato'),
    path('contrato_view_for_name/<str:name>', views.contrato_view_for_name, name='contrato_view_name'),
    path('colaborador/<int:pk>/update/', views.colaboradorUpdateView, name='colaborador-update'),
    path('delete/<int:id>', views.deleteColaborador, name="delete-colaborador"),
    # path('filtro/<str:classificacao>', views.filtro, name='filtro'),
    path('filtros/', views.filtrar_colaborador, name='filtros'),
    path('buscar', views.buscar, name='buscar'),
]
