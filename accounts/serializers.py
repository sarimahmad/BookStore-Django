from rest_framework import serializers
from accounts.models import StoreUser
from django.utils.translation import gettext_lazy as _


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6, write_only=True, required=True)

    class Meta:
        model = StoreUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        min_length=6,
        write_only=True
    )

    def run_validation(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            try:
                user = StoreUser.objects.get(email=email)
            except Exception as e:
                raise serializers.ValidationError({'message': 'User Does not Exit'})

            if not user.check_password(password):
                raise serializers.ValidationError({'message': 'Password is Incorrect.'})

        else:
            raise serializers.ValidationError({'message': 'Must include "email" and "password".'})

        data['user'] = user
        return data
