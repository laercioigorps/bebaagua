from django.urls import path
from .views import CriarPerfilView, ListarPerfisView, DetalhePerfilView

app_name = "perfil"
urlpatterns = [
    path("", view=CriarPerfilView.as_view(), name="criar_perfil"),
    path("listar/", view=ListarPerfisView.as_view(), name="listar_perfis"),
    path("<str:username>/", view=DetalhePerfilView.as_view(), name="detalhe_perfil"),
]
