from rest_framework import serializers
from django.contrib.auth.models import Group
from registration.models import player, society, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class PlayerRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = player
        fields = ['user', 'name', 'email', 'admissionNo', 'contact', 'college']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_obj = User.objects.create_user(**user_data)
        Player = player.objects.create(user=user_obj, **validated_data)
        users_group = Group.objects.get(name='Player')
        users_group.user_set.add(user_obj)
        Player.save()
        return Player


class SocietyRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = society
        fields = ['name', 'email', 'description', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_obj = User.objects.create_user(**user_data)
        Society = society.objects.create(user=user_obj, **validated_data)
        users_group = Group.objects.get(name='Society')
        users_group.user_set.add(user_obj)
        Society.save()
        return Society


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'password', ]

        extra_kwargs = {
            'password': {'write_only': True}
        }
