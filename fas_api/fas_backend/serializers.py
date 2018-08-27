from rest_framework import serializers
from fas_backend.models import FasApp, FasUser
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class FasAppSerializer(serializers.ModelSerializer):
#	name = serializers.NameField(
#			required=True,
#			validators=[UniqueValidator(queryset=FasApp.objects.all())]
#                )
	class Meta:
		model = FasApp
		fields = ('created', 'name', 'url', 'repo', 'size',)

from django.contrib.auth.models import User

class FasUserSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(
			required=True,
			validators=[UniqueValidator(queryset=FasUser.objects.all())]
		)
	username = serializers.CharField(
			validators=[UniqueValidator(queryset=FasUser.objects.all())]
		)
	password = serializers.CharField(min_length=1)

	def create(self, validated_data):
		user = FasUser.objects.create_user(
					validated_data['username'],
					validated_data['email'],
					validated_data['password']
				)
		return user

	class Meta:
		model = FasUser
		fields = ('id', 'created', 'email', 'password', 'username')

	def perform_create(self, serializer):
		serializer.save()
