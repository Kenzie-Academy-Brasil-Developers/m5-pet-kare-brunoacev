from rest_framework import serializers
from groups.serializers import GroupSerializer
from pets.models import Pet, Sex
from groups.models import Group
from traits.models import Trait
from traits.serializers import TraitSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=Sex.choices,
        default=Sex.Not_Informed,
    )
    group = GroupSerializer()
    traits_count = serializers.SerializerMethodField(
        method_name="trait_count",
        read_only=True,
    )
    traits = TraitSerializer(many=True)

    def trait_count(self, obj: Pet) -> int:
        return len(obj.traits.all())

    def create(self, validated_data: dict) -> Pet:
        group_dict = validated_data.pop("group")
        traits_list = validated_data.pop("traits")
        group = Group.objects.get_or_create(**group_dict)[0]
        pet = Pet.objects.create(**validated_data, group=group)
        for trait in traits_list:
            trait_obj = Trait.objects.get_or_create(**trait)[0]
            pet.traits.add(trait_obj)
        return pet

    def update(self, instance: Pet, validated_data: dict) -> Pet:
        if "group" in validated_data:
            group_dict = validated_data.pop("group")
            group_obj = Group.objects.get_or_create(**group_dict)[0]
            instance.group = group_obj
        if "traits" in validated_data:
            traits_list = validated_data.pop("traits")
            for trait in traits_list:
                trait_obj = Trait.objects.get_or_create(**trait)[0]
                instance.traits.clear()
                instance.traits.add(trait_obj)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance