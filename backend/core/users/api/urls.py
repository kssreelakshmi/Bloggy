from django.urls import path
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('auth/google/login/', GoogleLoginView.as_view(), name='google_login'),
    path('auth/google/callback/', GoogleCallbackView.as_view(), name='google_callback'),
]