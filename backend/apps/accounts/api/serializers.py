from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from apps.accounts.models import User, Address


# -------------------------------------------------------------------
# User Serializer
# -------------------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


# -------------------------------------------------------------------
# Address Serializer
# -------------------------------------------------------------------

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["user"]


# -------------------------------------------------------------------
# Register Serializer
# -------------------------------------------------------------------

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )