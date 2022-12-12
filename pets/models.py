from django.db import models


class Sex(models.TextChoices):
    Male = "Male"
    Female = "Female"
    Not_Informed = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=30,
        choices=Sex.choices,
        default=Sex.Not_Informed,
    )
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        related_name="groups",
    )
    traits = models.ManyToManyField(
        "traits.Trait",
        related_name="traits",
    )