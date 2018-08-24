from rest_framework import serializers
from fas_backend.models import FasApp, FasUser
from django.contrib.auth.models import User

class FasAppSerializer(serializers.ModelSerializer):
        owner = serializers.ReadOnlyField(source='owner.username')

        class Meta:
                model = FasApp
                fields = ('id', 'created', 'name', 'url', 'repo', 'size')
                owner = serializers.ReadOnlyField(source='owner.username')


class FasUserSerializer(serializers.ModelSerializer):
        apps = serializers.PrimaryKeyRelatedField(many=True, queryset=FasApp.objects.all())

        class Meta:
                model = FasUser
                fields = ('id', 'name', 'apps', 'created', )