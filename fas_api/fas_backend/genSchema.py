def get_man_schema():
    '''
    user creation schema
    '''
    # TODO : make this function obsolete
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

