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
        Player_obj = player.objects.create(user=user_obj, **validated_data)
        Group.objects.get(name='Player').user_set.add(user_obj)
        Player_obj.save()
        return Player_obj


class SocietyRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = society
        fields = ['name', 'email', 'description', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_obj = User.objects.create_user(**user_data)
        Society_obj = society.objects.create(user=user_obj, **validated_data)
        Group.objects.get(name='Society').user_set.add(user_obj)
        Society_obj.save()
        return Society_obj


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'password', ]

        extra_kwargs = {
            'password': {'write_only': True}
        }
