#views.py
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.conf import settings
import stripe
from rest_framework.decorators import action
from django.contrib.gis.geos import Point
from .models import User, Driver, Passenger, Ride, Post, Comment, RideGroupChat, Payment
from .serializers import UserSerializer, DriverSerializer, PassengerSerializer, RideSerializer, PostSerializer, CommentSerializer, RideGroupChatSerializer, PaymentSerializer
import random
from twilio.rest import Client
from django.core.cache import cache

stripe.api_key = settings.STRIPE_SECRET_KEY

# User registration
class InitialUserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if phone number is already registered
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({'error': 'Phone number is already registered'}, status=status.HTTP_400_BAD_REQUEST)

        # Send SMS verification code
        verification_code = str(random.randint(100000, 999999))
        cache.set(phone_number, verification_code, timeout=300)  # Cache for 5 minutes

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f'Your verification code is {verification_code}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        return Response({'message': 'Verification code sent'}, status=status.HTTP_200_OK)

class CompleteUserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('verification_code')

        if not phone_number or not verification_code:
            return Response({'error': 'Phone number and verification code are required'}, status=status.HTTP_400_BAD_REQUEST)

        stored_verification_code = cache.get(phone_number)

        if stored_verification_code == verification_code:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=True, methods=['get'])
    def rides(self, request, pk=None):
        driver = self.get_object()
        rides = Ride.objects.filter(driver=driver)
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data)

class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

    @action(detail=True, methods=['post'])
    def update_location(self, request, pk=None):
        ride = self.get_object()
        lat = request.data.get('latitude')
        lon = request.data.get('longitude')
        if lat and lon:
            ride.current_location = Point(float(lon), float(lat))
            ride.save()
            return Response({'status': 'Location updated'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def get_location(self, request, pk=None):
        ride = self.get_object()
        if ride.current_location:
            return Response({'latitude': ride.current_location.y, 'longitude': ride.current_location.x}, status=status.HTTP_200_OK)
        return Response({'error': 'Location not available'}, status=status.HTTP_404_NOT_FOUND)

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

class SendSMSVerificationView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        verification_code = str(random.randint(100000, 999999))
        
        # Save the verification code in cache for later verification
        cache.set(phone_number, verification_code, timeout=300)  # Cache for 5 minutes
        
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f'Your verification code is {verification_code}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        
        return Response({'message': 'Verification code sent'}, status=status.HTTP_200_OK)


class VerifySMSCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('verification_code')
        
        if not phone_number or not verification_code:
            return Response({'error': 'Phone number and verification code are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        stored_verification_code = cache.get(phone_number)
        
        if stored_verification_code == verification_code:
            return Response({'message': 'Phone number verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
