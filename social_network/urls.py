from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import PostViewSet, UserActivityView, SignUp, AnaliticsView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = router.urls
urlpatterns += [
    path('activity/', UserActivityView.as_view(), name='user_activity'),
    path('sign_up/', SignUp.as_view(), name='sign-up'),
    path('analitics/', AnaliticsView.as_view(), name='analitics'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
