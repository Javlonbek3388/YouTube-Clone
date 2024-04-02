from django.urls import path
from .views import SignUpApiView, VerifyCodeApiView, PersonalDataUpdadeApiView, LoginApiView, LogoutApiView, UpdateAccessTokenView

urlpatterns = [
    path('signup/', SignUpApiView.as_view()),
    path('code_verify/', VerifyCodeApiView.as_view()),
    path('personal_data/', PersonalDataUpdadeApiView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('logout/', LogoutApiView.as_view()),
    path('update-token/', UpdateAccessTokenView.as_view())
]
