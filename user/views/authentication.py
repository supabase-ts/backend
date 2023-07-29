from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from user.serializers.authentication import RegisterSerializer, LoginSerializer
from user.serializers.features import UserSerializer


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the user
        user = serializer.save()

        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = data['user']
        access_token = data['access_token']

        user.token = access_token
        user.save()

        return Response({
            "message": "Logged in successfully",
            "access_token": access_token,
            "user": UserSerializer(user).data,
        }, status=status.HTTP_200_OK)
