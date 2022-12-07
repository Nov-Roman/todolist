from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

USER_MODEL = get_user_model()


class PasswordField(serializers.CharField):

    def __init__(self, **kwargs):
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class RegistSerialiser(serializers.ModelSerializer):
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    def validate(self, attrs: dict):
        if attrs["password"] != attrs["password_repeat"]:
            raise serializers.ValidationError("Password must match")
        return attrs

    def create(self, validated_data: dict):
        del validated_data["password_repeat"]
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    class Meta:
        model = USER_MODEL
        fields = ("id", "username", "first_name", "last_name", "email", "password", "password_repeat")


class LoginSerialiser(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    def create(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if not user:
            raise AuthenticationFailed
        return user

    class Meta:
        model = USER_MODEL
        fields = ("username", "password")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ("id", "username", "first_name", "last_name", "email")


class UpdatePasswordSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)

    def validate(self, attrs: dict):
        if not (user := attrs["user"]):
            raise NotAuthenticated
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"old password": "field is incorrect"})
        return attrs

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data["new_password"])
        instance.save(update_fields=("password",))
        return instance
