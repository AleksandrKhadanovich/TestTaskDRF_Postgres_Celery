from django.urls import path
from users.views import *
# from django.contrib import admin
# from django.conf.urls import url,patterns
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'support'

# URL patterns of views created
urlpatterns = [
    path('new/', CommCreateView.as_view()),  # api/v1/support/new/ - to create ticket
    path('list/', CommListView.as_view()),  # api/v1/support/list/ - to list user's own tickets
    path('lstadm/', CommListViewAdmin.as_view()),  # api/v1/support/lstadm/ - to view all tickets for admin
    path('lstadm/<int:pk>/', CommDetailView.as_view()),  # answer ticket and change status for definite ticket №
    path('usernew/', CreateUserView.as_view()),  # api/v1/support/usernew/ - to create new user
    path('user/login/', LoginAPIView.as_view()),  # api/v1/support/usernew/ - to get JWT token for user

    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
