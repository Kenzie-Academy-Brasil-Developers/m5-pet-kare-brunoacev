from django.forms import ValidationError
from django.test import TestCase
from pets.models import Pet
from groups.models import Group
from traits.models import Trait
from django.db.utils import IntegrityError


class PetModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.pet_data = {
            "name": "Seraphim",
            "age": 1,
            "weight": 20,
            "sex": "Male",
            "group": {"scientific_name": "canis familiaris"},
            "traits": [{"name": "clever"}, {"name": "friendly"}],
        }
        cls.group_dict = cls.pet_data.pop("group")
        cls.traits_list = cls.pet_data.pop("traits")
        cls.pet_group = Group.objects.get_or_create(**cls.group_dict)[0]
        cls.my_pet = Pet.objects.create(**cls.pet_data, group=cls.pet_group)
        for trait in cls.traits_list:
            trait_obj = Trait.objects.get_or_create(**trait)[0]
            cls.my_pet.traits.add(trait_obj)

    def test_pet_objects_representation(self):
        """
        Verifica se a representação de objetos `Pet` está como esperado
        """
        expected = f"<Pet: {self.my_pet}>"
        resulted = repr(self.my_pet)

        msg = "Verifique se a representação de objetos `Pet` está de acordo"
        self.assertEqual(expected, resulted, msg)

    def test_if_empty_objects_can_be_created(self):
        """
        Verifica se é possível criar um pet com campos vazios
        """
        pet_data = {
            "name": "Seraphim",
            "age": 1,
            "weight": 20,
        }
        pet = Pet(**pet_data)

        self.assertRaises(ValidationError, pet.clean_fields)