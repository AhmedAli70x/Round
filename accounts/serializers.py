from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class AccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2','is_staff']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff' :{'read_only': True}
        }

    def validate_email(self, email):
        lower_email = email.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return lower_email

    def save(self):
        user = User()
        user.username = self.validated_data['username']
        user.email = self.validated_data['email'].lower()
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        # Check if email domain @company.com & assign is_staff True
        domain = user.email.split('@')[1]
        if domain == 'company.com':
            user.is_staff = True
        else:
            user.is_staff = False

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        user.set_password(password)
        user.save()

        return user
