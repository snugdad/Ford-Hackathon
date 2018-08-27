from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class FasUser(AbstractUser):
        id = models.AutoField(primary_key=True)
        created = models.DateTimeField(auto_now_add=True)
        name = models.CharField(max_length=100)

        class Meta:
                ordering = ('created',)
                default_permissions = ()
#                permissions = (('can_download', 'User can download media'),)

        def save(self, *args, **kwargs):
#                permission = Permission.objects.get(
#                        codename='can_download',
#			name='can download apps',
#                        content_type=ContentType.objects.get_for_model(FasApp),
#                )
#                self.user_permissions.add(permission)
                super(FasUser, self).save(*args, **kwargs)
        def has_change_permission(self, request, obj=None):
            if obj is not None and obj.created_by != request.user:
                return False
            return True

        def has_delete_permission(self, request, obj=None):
            if obj is not None and obj.created_by != request.user:
                return False
            return True

class FasApp(models.Model):
	id = models.AutoField(primary_key=True)
	# apps can have many users, many users can have apps
	fasusers = models.ManyToManyField(FasUser, related_name='FasUser')
	created = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=100)
	url = models.CharField(max_length=100)
	repo = models.CharField(max_length=100)
	size = models.CharField(max_length=10)
	appFile = models.FileField()

	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		'''
		on app creation, relate this app
		to all users
		'''
		fasusers = FasUser.objects.all()
		super(FasApp, self).save(*args, **kwargs)
