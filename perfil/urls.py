from django.urls import path
from .views import CriarPerfilView

app_name = "perfil"
urlpatterns = [
    path("", view=CriarPerfilView.as_view(), name="criar_perfil"),
]
