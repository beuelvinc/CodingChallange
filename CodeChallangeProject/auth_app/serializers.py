from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password',)
    #     extra_kwargs = {
    #         'password': {'write_only': True},
    #     }
    #
    # def validate_password(self, value: str) -> str:
    #     """
    #     Hash value passed by user.
    #     :param value: password of a user
    #     :return: a hashed version of the password
    #     """
    #     return make_password(value)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], password=validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # extra_kwargs = {
        #     'password': {'write_only': True},
        # }



