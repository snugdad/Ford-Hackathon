from django.db import models

#class FasApp(models.Model):
#        id = models.AutoField(primary_key=True)
#        created = models.DateTimeField(auto_now_add=True)
#        name = models.CharField(max_length=100)
#        url = models.CharField(max_length=100)
#        repo = models.CharField(max_length=100)
#        size = models.CharField(max_length=10)
#        appFile = models.FileField()
#
#        class Meta:
#                ordering = ('created',)
#
#        def save(self, *args, **kwargs):
#                super(FasApp, self).save(*args, **kwargs)
#
#class FasUser(AbstractUser):
#        id = models.AutoField(primary_key=True)
#        created = models.DateTimeField(auto_now_add=True)
#        name = models.CharField(max_length=100)
#        #age = models.IntegerField()
#        apps = models.ForeignKey(FasApp, on_delete=models.CASCADE)
#
#        class Meta:
#                ordering = ('created',)
#
#        def save(self, *args, **kwargs):
#                super(FasUser, self).save(*args, **kwargs)