from django.urls import path
from . import views

urlpatterns = [
    path('', views.colaboradorView, name='colaborador-lista'),
    path('colaboradorID/<int:id>', views.colaboradorIDview, name='colaborador-detalhe'),
    path('colaborador/create/', views.colaborador_create_view, name='colaborador-create'),
    path('colaborador/<int:pk>/update/', views.colaboradorUpdateView, name='colaborador-update'),
    path('delete/<int:id>', views.deleteColaborador, name="delete-colaborador"),
    path('contrato/create/', views.contrato_create_view, name='contrato-create'),
    path('contrato/', views.contrato_view, name='contrato'),
    path('contratoID/<int:id>', views.contrato_id_view, name='contrato-detalhe'),
    path('contrato/<int:pk>/update/', views.contrato_update_view, name='contrato_update'),
    path('contrato_view_for_name/<str:name>', views.contrato_view_for_name, name='contrato_view_name'),
    path('buscar', views.buscar, name='buscar'),
    path('desligados/', views.colaborador_desligado_view, name='colaborador-desligado'),
]
