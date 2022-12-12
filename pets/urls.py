from django.urls import path
from pets.views import PetView, PetViewTest

urlpatterns = [
    path("pets/", PetView.as_view()),
    path("pets/<int:pet_id>/", PetViewTest.as_view()),
]