from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AccountSerializer
# Create your views here.

from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Success', 'user': serializer.data, 'status': status.HTTP_201_CREATED}, status.HTTP_201_CREATED)
        return Response({'msg': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}, status.HTTP_201_CREATED )


class ListUsers(APIView):
    def get(self, request):
        """
        Return a list of all users.
        """
        try:
            users = User.objects.all().exclude(is_superuser=True).order_by('-is_staff')
            serializers = AccountSerializer(users, many=True)
            if len(users) > 0:
                return Response({'msg': 'Success', 'users': serializers.data, 'status': status.HTTP_200_OK}, status.HTTP_200_OK)
            else:
                return Response({'msg': 'No Users Found', 'users': serializers.data, 'status': status.HTTP_204_NO_CONTENT}, status.HTTP_204_NO_CONTENT)

        except:
            return Response({'msg': 'Invalid Query', 'users': [], 'status': status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)
