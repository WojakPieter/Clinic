from django.shortcuts import render
from django.db import models
from django.http import HttpResponse
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
import bcrypt
from datetime import datetime, timezone, timedelta
import jwt
import os
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

pepper = "bemsi projekt"

private_key_passphrase = b'BemsiProjekt123'
JWT_TOKEN_VALIDITY = 1
REFRESH_TOKEN_VALIDITY = 24
PATIENT_ROLE = "pacjent"
DOCTOR_ROLE = "lekarz"

def generate_tokens(login, role):
    module_dir = os.path.dirname(__file__)
    private_key_file_path = os.path.join(module_dir, 'bemsi-klucze')
    pem_bytes_file = open(private_key_file_path, "r")
    pem_bytes = pem_bytes_file.read().encode('utf-8')
    private_key = serialization.load_ssh_private_key(
        pem_bytes, password=private_key_passphrase, backend=default_backend()
    )
    token = jwt.encode({
            "login": login,
            "role": role,
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=JWT_TOKEN_VALIDITY),
            "iss": login,
            "iat": datetime.now(tz=timezone.utc)
        },
        private_key,
        algorithm="RS256"
    )
    refresh_token = jwt.encode({
            "login": login,
            "role": role,
            "refresh": True,
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=REFRESH_TOKEN_VALIDITY),
            "iss": login,
            "iat": datetime.now(tz=timezone.utc)
        },
        private_key,
        algorithm="RS256"
    )
    pem_bytes_file.close()
    RefreshToken(token=refresh_token).save()
    return token, refresh_token

def validate_token(token):
    module_dir = os.path.dirname(__file__)
    public_key_file_path = os.path.join(module_dir, 'bemsi-klucze.pub')
    public_key = open(public_key_file_path, "r").read().encode('utf-8')
    try:
        decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        return True
    except jwt.ExpiredSignatureError:
        return "expired"
    except Exception:
        return False

def decode_token(token):
    module_dir = os.path.dirname(__file__)
    public_key_file_path = os.path.join(module_dir, 'bemsi-klucze.pub')
    public_key = open(public_key_file_path, "r").read().encode('utf-8')
    try:
        decoded = jwt.decode(token, public_key, algorithms=["RS256"]) 
        if User.objects.filter(login=decoded['login']).count() == 0:
            return False
        return decoded
    except jwt.ExpiredSignatureError:
        return "expired"
    except Exception:
        return False


# Create your views here.
class LoginView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        if User.objects.filter(login=body['login']).count() == 0:
            return Response(status=status.HTTP_403_FORBIDDEN)
        user = User.objects.get(login=body['login'])
        password = body['password'] + pepper
        hashed = password.encode('utf-8')
        for i in range(3):
            hashed = bcrypt.hashpw(hashed, user.salt.encode('utf-8'))
        if hashed.decode('utf-8') == user.password:
            token, refresh_token = generate_tokens(user.login, user.role.name)
            # response = {"token": token, "refreshToken": refresh_token}
            # return Response(response, status=status.HTTP_200_OK)
            res = HttpResponse(token)
            max_age = 24 * 60 * 60
            res.set_cookie("refreshToken", refresh_token, httponly=True, secure=True, samesite=None, max_age=max_age, expires=datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age),"%a, %d-%b-%Y %H:%M:%S GMT"))
            return res
        return Response(status=status.HTTP_403_FORBIDDEN)
        

class RegisterView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        passwd = body["password"]
        if len(passwd) < 10:
            response = {"message":"Hasło musi mieć co najmniej 10 znaków"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        module_dir = os.path.dirname(__file__)
        common_passwords_file_path = os.path.join(module_dir, "100k-most-used-passwords-NCSC.txt")
        common_passwords_file = open(common_passwords_file_path, "r", encoding='utf-8')
        for line in common_passwords_file:
            if passwd == line.strip('\n'):
                common_passwords_file.close()
                response = {"message":"Hasło powszechnie używane"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        common_passwords_file.close()
        if len(body['login']) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(login=body["login"]).count() > 0:
            response = {"message":"Istnieje już użytkownik z danym loginem"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        salt = bcrypt.gensalt()
        password = passwd + pepper
        hashed = password.encode('utf-8')
        for i in range(3):
            hashed = bcrypt.hashpw(hashed, salt)
        if Role.objects.filter(name=body['role']).count() == 0:
            response = {"message":"Wskazana rola nie istnieje w systemie"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        role = Role.objects.get(name=body['role'])
        newUser = User(login=body['login'], role=role, password=hashed.decode('utf-8'), salt=salt.decode('utf-8'))
        newUser.save()
        return Response(status=status.HTTP_200_OK)

class GetUserView(APIView):
    def get(self, request):
        headers = request.headers
        try:
            if headers.get('Authorization')[0:7] != "Bearer ":
                raise KeyError
            token = headers.get('Authorization')[7:]
            decoded = decode_token(token)
            if decoded == "expired":
                response = {"message": "JWT Token expired"}
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            if decoded == False:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            user = User.objects.get(login=decoded["login"])
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES['refreshToken']
            decoded = decode_token(refresh_token)
            if decoded == "expired" or decoded == False:
                return Response(status.HTTP_401_UNAUTHORIZED)
            if decoded['refresh'] == True:
                new_token, new_refresh_token = generate_tokens(decoded['login'], decoded['role'])
                res = HttpResponse(new_token)
                res.set_cookie("refreshToken", new_refresh_token, httponly=True, secure=True, expires="1d", samesite=None)
                return res
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            
class GetNotesView(APIView):
    def get(self, request):
        headers = request.headers
        try:
            if headers.get('Authorization')[0:7] != "Bearer ":
                raise KeyError
            token = headers.get('Authorization')[7:]
            decoded = decode_token(token)
            if decoded == "expired":
                response = {"message": "JWT Token expired"}
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            if decoded == False:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            if decoded["role"] == PATIENT_ROLE:
                user = User.objects.get(login=decoded["login"])
                notes = Note.objects.filter(patient=user)
                serializer = NoteSerializer(notes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif decoded["role"] == DOCTOR_ROLE:
                user = User.objects.get(login=decoded["login"])
                notes = Note.objects.filter(doctor=user)
                serializer = NoteSerializer(notes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class GetPatientsView(APIView):
    def get(self, request):
        headers = request.headers
        try:
            if headers.get('Authorization')[0:7] != "Bearer ":
                raise KeyError
            token = headers.get('Authorization')[7:]
            decoded = decode_token(token)
            if decoded == "expired":
                response = {"message": "JWT Token expired"}
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            if decoded == False:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            if decoded["role"] == DOCTOR_ROLE:
                role = Role.objects.get(name=PATIENT_ROLE)
                patients = User.objects.filter(role=role)
                serializer = UserSerializer(patients, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class AddNoteView(APIView):
    def put(self, request):
        headers = request.headers
        body = json.loads(request.body)
        try:
            if headers.get('Authorization')[0:7] != "Bearer ":
                raise KeyError
            token = headers.get('Authorization')[7:]
            decoded = decode_token(token)
            if decoded == "expired":
                response = {"message": "JWT Token expired"}
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            if decoded == False:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            if User.objects.filter(login=body["notePatient"]).count() == 0:
                response = {"message", "Nie ma takiego użytkownika"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            patient = User.objects.get(login=body["notePatient"])
            if decoded["role"] == DOCTOR_ROLE:
                note = Note(content=body["noteContent"], patient=patient)
                note.doctor = User.objects.get(login=decoded["login"])
                note.creation_date = datetime.now()
                note.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
