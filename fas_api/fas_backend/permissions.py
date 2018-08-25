from rest_framework.compat import coreapi, coreschema
from rest_framework import permissions
from rest_framework.schemas import ManualSchema
from django.contrib.auth.models import Permission

def getPermit():
	permission = Permission.objects.create(
			codename='can_publish',
			name='Can Publish Posts',
			content_type=None,
		)
	return permission

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

def get_man_schema(opt=None):
    '''
    user creation schema
    '''
    # TODO : make this function obsolete
    if opt == 'login':
          return ManualSchema(
                        fields=[
                                coreapi.Field(
                                        name="username",
                                        required=True,
                                        location='form',
                                        schema=coreschema.String(
                                                title="Username",
                                                description="Valid username for authentication",
                                        ),
                                ),
                                coreapi.Field(
                                        name="password",
                                        required=True,
                                        location='form',
                                        schema=coreschema.String(
                                                title="Password",
                                                description="Valid password for authentication",
                                        ),
                                ),
                        ],
                        encoding="application/json",
                )	
    return ManualSchema(
                        fields=[
                                coreapi.Field(
                                        name="username",
                                        required=True,
                                        location='form',
                                        schema=coreschema.String(
                                                title="Username",
                                                description="Valid username for authentication",
                                        ),
                                ),
                                coreapi.Field(
                                        name="password",
                                        required=True,
                                        location='form',
                                        schema=coreschema.String(
                                                title="Password",
                                                description="Valid password for authentication",
                                        ),
                                ),
                                coreapi.Field(
                                        name="email",
                                        required=True,
                                        location='form',
                                        schema=coreschema.String(
                                                title="email",
                                                description="Valid email for authentication",
                                        ),
                                ),
                        ],
                        encoding="application/json",
                )
