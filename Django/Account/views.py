from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework import authentication, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, generics
from .models import ServiceUser
from .serializers import UserSerializer, UserSerializerWithToken
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


### User - Admin Rights ###
# FBV


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getUsersAdmin(request):
    users = ServiceUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getUserDetailAdmin(request, pk):
    user = ServiceUser.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    user = ServiceUser.objects.get(id=pk)

    data = request.data

    user.email = data["email"]
    user.first_name = data["firstName"]
    user.last_name = data["lastName"]
    user.is_pathologist = data["isPathologist"]

    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = ServiceUser.objects.get(id=pk)
    userForDeletion.delete()
    return Response("User was deleted")


### User - Profile Rights ###
# FBV
@api_view(["POST"])
def registerUser(request):

    data = request.data
    print(data)
    try:
        user = ServiceUser.objects.create(
            email=data["email"],
            first_name=data["firstName"],
            last_name=data["lastName"],
            password=make_password(data["password"]),  # Hash Password
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {"Detail": "Incorrect registration data"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


# Search User
class UserViewSetByName(generics.ListAPIView):
    queryset = ServiceUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name"]


class UserViewConsultants(generics.ListAPIView):
    queryset = ServiceUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]


class UserViewPathologists(generics.ListAPIView):
    queryset = ServiceUser.objects.filter()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    print(user)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    print(user)  # Old user data
    serializer = UserSerializerWithToken(user, many=False)
    # New token will be assgined with User Profile update

    data = request.data
    print(data)  # Changed user data

    user.email = data["email"]
    user.first_name = data["firstName"]
    user.last_name = data["lastName"]

    # Change password if specified
    if data["password"] != "":
        user.password = make_password(data["password"])

    user.save()
    print(user)  # New user data

    return Response(serializer.data)


# CBV
class GetUserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


## Main Menu
class MenuView(TemplateView):
    template_name = "Account/Account.html"
    model = ServiceUser
