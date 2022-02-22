from django.contrib.auth import authenticate
from rest_framework import serializers
from users.models import User, Comm


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=28,
        min_length=3,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'token')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CommCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comm
        fields = ('id', 'comment', 'user')


class CommListSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Comm
        fields = '__all__'


class CommListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comm
        fields = ('comment', 'answer', 'user')


class CommDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comm
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, write_only=True)
    password = serializers.CharField(max_length=30, write_only=True)
    email = serializers.CharField(max_length=40, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'An username is required to log in.')

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this name and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.')

        return {
            'username': user.username,
            'email': user.email,
            'token': user._generate_jwt_token()
        }
