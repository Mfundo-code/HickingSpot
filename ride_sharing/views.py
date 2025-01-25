#views.py
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import stripe
from .models import User, Driver, Passenger, Ride, Post, Comment, RideGroupChat, Payment
from .serializers import UserSerializer, DriverSerializer, PassengerSerializer, RideSerializer, PostSerializer, CommentSerializer, RideGroupChatSerializer, PaymentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

# Community Hub Views
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# Official Ride-Sharing Views
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

class RideGroupChatViewSet(viewsets.ModelViewSet):
    queryset = RideGroupChat.objects.all()
    serializer_class = RideGroupChatSerializer

# Payment Views
class CreatePaymentIntentView(APIView):
    def post(self, request, format=None):
        try:
            amount = int(request.data.get('amount', 0) * 100)  # Amount in cents
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card'],
            )
            return Response({'client_secret': payment_intent['client_secret']}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ConfirmPaymentView(APIView):
    def post(self, request, format=None):
        try:
            payment_intent_id = request.data.get('payment_intent_id')
            stripe_charge_id = stripe.PaymentIntent.confirm(payment_intent_id)['charges']['data'][0]['id']
            ride_id = request.data.get('ride_id')
            user = request.user
            ride = Ride.objects.get(id=ride_id)
            amount = request.data.get('amount')

            payment = Payment.objects.create(
                user=user,
                ride=ride,
                amount=amount,
                stripe_charge_id=stripe_charge_id
            )
            return Response(PaymentSerializer(payment).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
