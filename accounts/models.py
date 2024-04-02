from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
import uuid
import random
from rest_framework_simplejwt.tokens import RefreshToken

from datetime import datetime, timedelta
# Create your models here.
AUTH_TYPE = (
    ('google', 'google'),
    ('email', 'email')
)
AYTH_STATUS = (
    ('sent_email', 'sent_email'),
    ('verify_code', 'verify_code'),
    ('complate', 'complate'),
)

class User(AbstractUser, BaseModel):
    
    auth_type = models.CharField(max_length = 6, choices=AUTH_TYPE, null=True, blank=True)
    auth_status = models.CharField(max_length = 15, choices=AYTH_STATUS, default='sent_email')
    email = models.EmailField(null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to='user/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'heic', 'heif'])
    ])
    
    def __str__(self) -> str:
        return self.username
    
    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    
    def cheak_username(self):
        if not self.username:
            test_username = f'user-{uuid.uuid4().__str__().split("-")[1]}'
            while User.objects.filter(username=test_username):
                test_username = f"{test_username}{random.randint(0, 9)}"
            self.username = test_username
            
    def cheak_email(self):
        if self.email:
            test_email = self.email.lower()
            self.email = test_email
            
    def cheak_password(self):
        if not self.password:
            test_password = f'password-{uuid.uuid4().__str__().split("-")[1]}'
            self.password = test_password
            
    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)
            
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access' : str(refresh.access_token),
            'refresh' : str(refresh)
        }
        
    def create_code(self):
        code = "".join([str(random.randint(0, 10) % 10) for _ in range(6)])
        UserConfirmation.objects.create(
            user = self,
            code = code
        )
        return code
        
    def save(self, *args, **kwargs):
        self.clean()
        # if self.auth_status == 'complate':
        #     chanel = Chanel.objects.create(user = self, name = self.username)
        super(User, self).save(*args, **kwargs)
    
    def clean(self) -> None:
        self.cheak_username()
        self.cheak_email()
        self.cheak_password()
        self.hashing_password()

CODE_LIFETIME = 3       

class UserConfirmation(BaseModel):
    code = models.CharField(max_length = 6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'verify_code')
    code_lifetime = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.user.username

    def save(self, *args, **kwargs):
        self.code_lifetime = datetime.now() + timedelta(minutes=CODE_LIFETIME)
        super(UserConfirmation, self).save(*args, **kwargs)