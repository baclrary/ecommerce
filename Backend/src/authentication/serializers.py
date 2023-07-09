from rest_framework import serializers
from users.models import CustomUser, SellerProfile, BuyerProfile


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "phone", "type", "password"]

    def validate_email(self, value):
        # This method is provided by Django Rest Framework for field level validation.
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(f"User with email - {value} - is already registered")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(email=validated_data["email"],
                                              password=validated_data["password"],
                                              phone=validated_data["phone"],
                                              type=validated_data["type"])
        user.set_password(validated_data["password"])
        user.is_active = True
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "phone", "type"]


class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = SellerProfile
        fields = "__all__"


class BuyerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BuyerProfile
        fields = "__all__"
