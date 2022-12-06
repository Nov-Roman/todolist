from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

USER_MODEL = get_user_model()


class RegistSerialiser(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password_repeat = attrs.pop('password_repeat')

        if password != password_repeat:
            raise serializers.ValidationError('Password do not match')
        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError({'password': e.args[0]})
        return attrs

    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data['password'] = make_password(password)
        isinstance = super().create(validated_data)
        return isinstance

    class Meta:
        model = USER_MODEL
        fields = '__all__'


class LoginSerialiser(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def create(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if not user:
            raise AuthenticationFailed
        return user

    class Meta:
        model = USER_MODEL
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UpdatePasswordSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: dict):
        if not (user := attrs["user"]):
            raise NotAuthenticated
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"old password": "field is incorrect"})
        return attrs

    def create(self, validated_data: dict):
        raise NotImplementedError

    def update(self, instance, validated_data: dict):
        instance.password = make_password(validated_data["new_password"])
        instance.save(update_fields=("password",))
        return instance
