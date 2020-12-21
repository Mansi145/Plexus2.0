from rest_framework.permissions import BasePermission
from registration.models import player, society
from django.contrib.auth.models import Group


class IsPlayer(BasePermission):
    def has_permission(self, request, view):
        isPlayer = Group.objects.get(name='Player').user_set.filter(id=request.user.id).exists()
        if isPlayer:
            request.__setattr__('user_group', 'Player')
        return request.user and isPlayer


class IsSociety(BasePermission):
    def has_permission(self, request, view):
        isSociety = Group.objects.get(name='Society').user_set.filter(id=request.user.id).exists()
        if isSociety:
            request.__setattr__('user_group', 'Society')
        return request.user and isSociety
