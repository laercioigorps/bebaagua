from django.urls import path
from .views import CriarPerfilView, ListarPerfisView

app_name = "perfil"
urlpatterns = [
    path("", view=CriarPerfilView.as_view(), name="criar_perfil"),
    path("listar/", view=ListarPerfisView.as_view(), name="listar_perfis"),
]
