#ride_sharing/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InitialUserRegistrationView, CompleteUserRegistrationView, DriverViewSet, PassengerViewSet, RideViewSet, PostViewSet, CommentViewSet, RideGroupChatViewSet
from .views import SendSMSVerificationView, VerifySMSCodeView

router = DefaultRouter()
router.register(r'drivers', DriverViewSet)
router.register(r'passengers', PassengerViewSet)
router.register(r'rides', RideViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'group_chats', RideGroupChatViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Router URLs
    path('initial_register/', InitialUserRegistrationView.as_view(), name='initial_register'),
    path('complete_register/', CompleteUserRegistrationView.as_view(), name='complete_register'),
    path('send_verification_code/', SendSMSVerificationView.as_view(), name='send_verification_code'),
    path('verify_sms_code/', VerifySMSCodeView.as_view(), name='verify_sms_code'),
]
