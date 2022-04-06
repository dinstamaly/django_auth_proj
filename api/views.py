from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from firebase_admin import auth
from django.contrib.auth import get_user_model

from api.serializers import UserSerializer


class AuthenticatedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'You Are Authenticated', 'user': request.user.username})


class RegisterUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        print(request.user.username)
        User = get_user_model()
        if user_serializer.is_valid():
            user = User.objects.create(username=user_serializer.data["username"],
                                       )
            firebase_data = auth.create_user(
                email=user_serializer.data["email"],
                email_verified=True,
                password=user_serializer.data["password"],
                disabled=False
            )
            user.email = firebase_data.email
            user.set_password(user_serializer.validated_data["password"])
            user.save()
        return Response({'message': 'User Registered'})
