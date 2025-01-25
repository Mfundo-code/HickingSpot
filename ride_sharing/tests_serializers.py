#tests_serializers.py
from django.test import TestCase
from rest_framework.test import APITestCase
from .models import User, Driver, Passenger, Ride, Post, Comment, RideGroupChat, Payment
from .serializers import UserSerializer, DriverSerializer, PassengerSerializer, RideSerializer, PostSerializer, CommentSerializer, RideGroupChatSerializer, PaymentSerializer

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='johndoe',
            password='password123',
            phone_number='1234567890'
        )
        self.serializer = UserSerializer(instance=self.user)

    def test_user_serializer(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'username', 'phone_number', 'is_driver', 'is_passenger'})
        self.assertEqual(data['username'], 'johndoe')

class DriverSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='johndoe',
            password='password123',
            phone_number='1234567890'
        )
        self.driver = Driver.objects.create(
            user=self.user,
            license_number="ABC12345",
            vehicle_details="Sedan, White, 2019",
            available_seats=4,
            is_available=True
        )
        self.serializer = DriverSerializer(instance=self.driver)

    def test_driver_serializer(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'user', 'license_number', 'vehicle_details', 'available_seats', 'is_available'})
        self.assertEqual(data['user']['username'], 'johndoe')

class PassengerSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='janedoe',
            password='password123',
            phone_number='0987654321'
        )
        self.passenger = Passenger.objects.create(
            user=self.user,
            emergency_contact='911',
            live_location_sharing=True
        )
        self.serializer = PassengerSerializer(instance=self.passenger)

    def test_passenger_serializer(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'user', 'emergency_contact', 'live_location_sharing'})
        self.assertEqual(data['user']['username'], 'janedoe')

class RideSerializerTest(TestCase):
    def setUp(self):
        self.driver_user = User.objects.create_user(
            username='johndoe',
            password='password123',
            phone_number='1234567890'
        )
        self.passenger_user = User.objects.create_user(
            username='janedoe',
            password='password123',
            phone_number='0987654321'
        )
        self.driver = Driver.objects.create(
            user=self.driver_user,
            license_number="ABC12345",
            vehicle_details="Sedan, White, 2019",
            available_seats=4,
            is_available=True
        )
        self.passenger = Passenger.objects.create(
            user=self.passenger_user,
            emergency_contact='911',
            live_location_sharing=True
        )
        self.ride = Ride.objects.create(
            driver=self.driver,
            pickup_location='POINT(1 1)',
            dropoff_location='POINT(2 2)',
            distance=10.0,
            price_per_head=100.0,
            departure_time='2025-01-16T08:30:00Z',
            ride_status='Available'
        )
        self.ride.passengers.add(self.passenger)
        self.serializer = RideSerializer(instance=self.ride)

    def test_ride_serializer(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'driver', 'passengers', 'pickup_location', 'dropoff_location', 'distance', 'price_per_head', 'departure_time', 'ride_status'})
        self.assertEqual(data['driver']['user']['username'], 'johndoe')
        self.assertEqual(len(data['passengers']), 1)
        self.assertEqual(data['passengers'][0]['user']['username'], 'janedoe')

class PostSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='johndoe',
            password='password123',
            phone_number='1234567890'
        )
        self.post = Post.objects.create(
            author=self.user,
            content="This is a test post",
            timestamp='2025-01-16T08:30:00Z'
        )
        self.serializer = PostSerializer(instance=self.post)

    def test_post_serializer(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'author', 'content', 'timestamp'})
        self.assertEqual(data['author']['username'], 'johndoe')

class CommentSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='johndoe',
            password='password123',
            phone_number='1234567890'
        )
        self.post = Post.objects.create(
            author=self.user,
            content="This is a test post",
            timestamp='2025-01-16T08:30:00Z'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="This is a test comment",
            timestamp='2025-01-16T08:35:00Z'
        )
        self.serializer = CommentSerializer(instance=self.comment)

    def test_comment_serializer(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'post', 'author', 'content', 'timestamp'})
        self.assertEqual(data['author']['username'], 'johndoe')
        self.assertEqual(data['post']['author']['username'], 'johndoe')

class RideGroupChatSerializerTest(TestCase):
    def setUp(self):
        self.driver_user = User.objects.create_user(
            username='johndoe',
            password='password123',
            phone_number='1234567890'
        )
        self.passenger_user = User.objects.create_user(
            username='janedoe',
            password='password123',
            phone_number='0987654321'
        )
        self.driver = Driver.objects.create(
            user=self.driver_user,
            license_number="ABC12345",
            vehicle_details="Sedan, White, 2019",
            available_seats=4,
            is_available=True
        )
        self.passenger = Passenger.objects.create(
            user=self.passenger_user,
            emergency_contact='911',
            live_location_sharing=True
        )
        self.ride = Ride.objects.create(
            driver=self.driver,
            pickup_location='POINT(1 1)',
            dropoff_location='POINT(2 2)',
            distance=10.0,
            price_per_head=100.0,
            departure_time='2025-01-16T08:30:00Z',
            ride_status='Available'
        )
        self.ride.passengers.add(self.passenger)
        self.chat = RideGroupChat.objects.create(
            ride=self.ride,
            driver=self.driver,
            message="This is a test message",
            timestamp='2025-01-16T08:40:00Z'
        )
        self.chat.passengers.add(self.passenger)
        self.serializer = RideGroupChatSerializer(instance=self.chat)

    def test_ride_group_chat_serializer(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'ride', 'passengers', 'driver', 'message', 'timestamp'})
        self.assertEqual(data['driver']['user']['username'], 'johndoe')
        self.assertEqual(len(data['passengers']), 1)
        self.assertEqual(data['passengers'][0]['user']['username'], 'janedoe')
        self.assertEqual(data['ride']['driver']['user']['username'], 'johndoe')

class PaymentSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='johndoe',
            password='password123',
            phone_number='1234567890'
        )
        self.driver = Driver.objects.create(
            user=self.user,
            license_number="ABC12345",
            vehicle_details="Sedan, White, 2019",
            available_seats=4,
            is_available=True
        )
        self.ride = Ride.objects.create(
            driver=self.driver,
            pickup_location='POINT(1 1)',
            dropoff_location='POINT(2 2)',
            distance=10.0,
            price_per_head=100.0,
            departure_time='2025-01-16T08:30:00Z',
            ride_status='Available'
        )
        self.payment = Payment.objects.create(
            user=self.user,
            ride=self.ride,
            amount=100.0,
            stripe_charge_id='ch_123456789',
            created_at='2025-01-16T08:45:00Z'
        )
        self.serializer = PaymentSerializer(instance=self.payment)

    def test_payment_serializer(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'user', 'ride', 'amount', 'stripe_charge_id', 'created_at'})
        self.assertEqual(data['user']['username'], 'johndoe')
        self.assertEqual(data['ride']['driver']['user']['username'], 'johndoe')
