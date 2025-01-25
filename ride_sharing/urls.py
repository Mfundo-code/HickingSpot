#ride_sharing/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DriverViewSet, PassengerViewSet, RideViewSet, PostViewSet, CommentViewSet, RideGroupChatViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'passengers', PassengerViewSet)
router.register(r'rides', RideViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'group_chats', RideGroupChatViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
]
