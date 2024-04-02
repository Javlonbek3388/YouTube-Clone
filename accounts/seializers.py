from rest_framework import serializers
from .models import User
from content.models import Channel

from base.utility import check_email, send_email, check_username, check_user
from rest_framework.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import update_last_login


class SingUpSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'id',
            'auth_status',
            'email'
        )
        extra_kwargs = {
            'id' : {'read_only' : True},
            'auth_status' : {'read_only' : True, 'required' : False}
        }
    
    
    def create(self, validated_data):
        user = super(SingUpSerializer, self).create(validated_data)
        code = user.create_code()
        send_email(user.email, code)
        user.save()
        return user
    
    
    
    def to_representation(self, instance):
        data = super(SingUpSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data
    
    # def validate(self, data):
    #     super(SingUpSerializer, self).validate(data)
    #     data = self.auth_email(data)
        
    #     return data
        
        
        
    # @staticmethod
    # def auth_email(data):
    #     email = data.get('email')
    #     valid_email = check_email(email)
    #     if not valid_email:
    #         data = {
    #             'status' : False,
    #             'message' : "Invalid Email"
    #         }
    #         raise ValidationError(data)
    #     return data
    
    
    
class PersonalDataSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    photo = serializers.ImageField(validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'heic', 'heif'])
    ])
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password')
        if password:
            validate_password(password)
            validate_password(confirm_password)
        
        if password != confirm_password:
            data = {
                'status' : False,
                'message' : 'Parollar mos emas'
            }
            raise ValidationError(data)
        
        
                
        return data
    
    
    def validate_username(self, username):
        
        if not check_username(username):
            data = {
                'status' : False,
                'message' : 'Usrname yaroqsiz'
            }
            raise ValidationError(data)
        if User.objects.filter(username=username).exists():
            data = {
                'status' : False,
                'message' : 'Usrname mavjud'
            }
            raise ValidationError(data)
        
        return username
    
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        instance.photo = validated_data.get('photo', instance.photo)
        if instance.auth_status == 'verify_code':
            instance.auth_status = 'complate'
            chanel = Channel.objects.create(user = instance, name = instance.username)

        instance.save()

        
        return instance
        
        

class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs) -> None:
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['username'] = serializers.CharField(required = False, read_only=True)
        self.fields['user_input'] = serializers.CharField(required = True)
    
    def auth_validate(self, data):
        user_input = data.get('user_input')
        password = data.get('password')
        
        if check_user(user_input) == 'email':
         
            username = self.auth_user(user_input)
            
        elif check_user(user_input) == "username":
            
            username = user_input
            
        else:
            data = {
                'status' : False,
                'message' : 'Siz Kiritgan malumotlarga mos user topilmadi iltios qaytadan tekshirib kiriting!'
            }
            raise ValidationError(data)
        
        
        
        user_kwargs = {
            self.username_field : username,
            "password" : password
        }
        
        user_ch = User.objects.get(username = username)
        if user_ch.auth_status != "complate":
            data = {
            'status' : False,
                'message' : 'Siz hali Toliq ruyxatdan otmagansiz!'
            }
            raise ValidationError(data) 
        
        user = authenticate(**user_kwargs)
        if user is not None:
            self.user = user
        else:
            data = {
            'status' : False,
                'message' : 'User yoki parol xato'
            }
            raise ValidationError(data) 
        
    def auth_user(self, email):
        user = User.objects.get(email = email)
        if not user:
            data = {
            'status' : False,
                'message' : 'Siz Kiritgan malumotlarga mos user topilmadi iltios qaytadan tekshirib kiriting!'
            }
            raise ValidationError(data) 
        return user.username
    
    
    
    
    def validate(self, data):
        self.auth_validate(data)
        
        data = self.user.token()
        data['full_name'] = self.user.full_name
        
        return data
    
class LogoutSerializers(serializers.Serializer):
    refresh = serializers.CharField()
    
    
class UpdateAccessTokenSerializers(TokenRefreshSerializer):
    
    def validate(self, data):
        data = super().validate(data)
        acces_token_instance = AccessToken(data['access'])
        user_id = acces_token_instance['user_id']
        
        user = get_object_or_404(User, id = user_id)
        update_last_login(None, user)
        
        return data