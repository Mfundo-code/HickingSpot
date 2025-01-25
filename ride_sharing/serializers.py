#serializers.py
from rest_framework import serializers
from .models import User, Driver, Passenger, Ride, Post, Comment, RideGroupChat, Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'is_driver', 'is_passenger']

class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Include nested user information

    class Meta:
        model = Driver
        fields = ['id', 'user', 'license_number', 'vehicle_details', 'available_seats', 'is_available']

class PassengerSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Include nested user information

    class Meta:
        model = Passenger
        fields = ['id', 'user', 'emergency_contact', 'live_location_sharing']

class RideSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()  # Include nested driver information
    passengers = PassengerSerializer(many=True)  # Include nested passenger information

    class Meta:
        model = Ride
        fields = ['id', 'driver', 'passengers', 'pickup_location', 'dropoff_location', 'distance', 'price_per_head', 'departure_time', 'ride_status']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()  # Include nested author information

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'timestamp']

class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer()  # Include nested post information
    author = UserSerializer()  # Include nested author information

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'timestamp']

class RideGroupChatSerializer(serializers.ModelSerializer):
    ride = RideSerializer()  # Include nested ride information
    passengers = PassengerSerializer(many=True)  # Include nested passenger information
    driver = DriverSerializer()  # Include nested driver information

    class Meta:
        model = RideGroupChat
        fields = ['id', 'ride', 'passengers', 'driver', 'message', 'timestamp']

class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Include nested user information
    ride = RideSerializer()  # Include nested ride information

    class Meta:
        model = Payment
        fields = ['id', 'user', 'ride', 'amount', 'stripe_charge_id', 'created_at']
