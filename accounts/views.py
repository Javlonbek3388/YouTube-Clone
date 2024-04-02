from django.shortcuts import render
from .seializers import SingUpSerializer, PersonalDataSerializer, LoginSerializer, LogoutSerializers, UpdateAccessTokenSerializers
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from .models import User
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class SignUpApiView(CreateAPIView):
    permission_classes = (AllowAny, )
    queryset = User.objects.all()
    serializer_class = SingUpSerializer
    
    
class VerifyCodeApiView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')
        self.check_code(user, code)
        
        data = {
            'status' : True,
            'auth_status' : user.auth_status,
            'access' : user.token()['access'],
            'refresh' : user.token()['refresh']
        }
        return Response(data)
        
    @staticmethod
    def check_code(user, code):
        verify_code = user.verify_code.filter(code_lifetime__gte=datetime.now(), code=code, is_confirmed=False)
        
        if not verify_code.exists():
            data = {
                'status' : False,
                'message' : "Code vaqti tugagan yoki Code yaroqsiz"
            }
            raise ValidationError(data)
        
        else:
            verify_code.update(is_confirmed=True)
            
        if user.auth_status == 'sent_email':
            user.auth_status = 'verify_code'
            user.save()
        return True
    

class PersonalDataUpdadeApiView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PersonalDataSerializer
    http_method_names = ['put', 'patch']
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        super(PersonalDataUpdadeApiView, self).update(request, *args, **kwargs)
        data = {
            'status' : True,
            'message' : 'Ruyxatdan muvafaqiyatli otdingiz',
            'auth_status' : self.request.user.auth_status
        }
        
        return Response(data)
    
    
    
    def partial_update(self, request, *args, **kwargs):
        super(PersonalDataUpdadeApiView, self).partial_update(request, *args, **kwargs)
        data = {
            'status' : True,
            'message' : 'Ruyxatdan muvafaqiyatli otdingiz',
            'auth_status' : self.request.user.auth_status
        }
        return Response(data)
    
    
class LoginApiView(TokenObtainPairView):
    serializer_class = LoginSerializer
    
    

class LogoutApiView(APIView):
    serializer_class = LogoutSerializers
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                "status" : True,
                "message" : "Siz tizimdan chiqdiz"
            }
            
            return Response(data, status=205)
        except Exception as e:
            data = {
                "status" : False,
                "message" : str(e)
            }
            return Response(data, status=400)
        
        
class UpdateAccessTokenView(TokenRefreshView):
    serializer_class = UpdateAccessTokenSerializers