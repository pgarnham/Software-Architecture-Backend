from django.urls import include, path
from rest_framework import routers
from chat import views
from django.contrib import admin
from rest_framework_simplejwt import views as jwt_views 

router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'rooms', views.RoomViewSet)

urlpatterns = [
    path('api/token/', 
         jwt_views.TokenObtainPairView.as_view(), 
         name ='token_obtain_pair'), 
    path('api/token/refresh/', 
         jwt_views.TokenRefreshView.as_view(), 
         name ='token_refresh'), 
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    path(r'^accounts/', include('allauth.urls'), name='socialaccount_signup'),
]
