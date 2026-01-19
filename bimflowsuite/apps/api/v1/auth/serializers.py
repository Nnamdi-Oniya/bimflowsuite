from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    """Login – Swagger shows editable username/password fields."""
    username = serializers.CharField(
        max_length=150,
        required=True,
        help_text="Username (e.g., admin)"
    )
    password = serializers.CharField(
        max_length=128,
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Password"
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            return attrs
        raise serializers.ValidationError("Both username and password are required.")

class RegisterSerializer(serializers.ModelSerializer):
    """Register – Swagger editable fields."""
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Password (min 8 chars)"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    """User + tokens output."""
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'access', 'refresh']
        read_only_fields = ['id', 'date_joined', 'access', 'refresh']

    def get_access(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def get_refresh(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh)