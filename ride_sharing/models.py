#models.py
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model (AbstractUser)
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    is_driver = models.BooleanField(default=False)
    is_passenger = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# Driver model
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=20)
    vehicle_details = models.TextField()
    available_seats = models.IntegerField()
    is_available = models.BooleanField(default=True)
    
    # Security fields for driver verification
    license_photo = models.ImageField(upload_to='driver_licenses/', null=True, blank=True)  # Made nullable
    driver_photo = models.ImageField(upload_to='drivers_photos/', null=True, blank=True)  # Made nullable

    def __str__(self):
        return f"Driver: {self.user.username}"

    def get_available_rides(self):
        return Ride.objects.filter(driver=self, ride_status="Available")

# Passenger model
class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emergency_contact = models.CharField(max_length=15)
    live_location_sharing = models.BooleanField(default=False)

    def __str__(self):
        return f"Passenger: {self.user.username}"

# Ride model
class Ride(models.Model):
    RIDE_STATUS_CHOICES = [
        ('Available', 'Available'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    passengers = models.ManyToManyField(Passenger)
    pickup_location = models.PointField()
    dropoff_location = models.PointField()
    distance = models.FloatField()
    price_per_head = models.DecimalField(max_digits=10, decimal_places=2)
    departure_time = models.DateTimeField()
    ride_status = models.CharField(max_length=20, choices=RIDE_STATUS_CHOICES, default='Available')
    current_location = models.PointField(null=True, blank=True)  # New field for live location updates

    def __str__(self):
        return f"Ride {self.id} with {self.driver.user.username}"

    def calculate_fare(self):
        if self.price_per_head < 30:
            return 30  # Base fare per person if it's less than 30
        return self.price_per_head * 1.6  # 160% of the distance traveled

    def is_available_for_passenger(self, passenger, requested_time):
        if self.ride_status != "Available":
            return False
        if self.departure_time != requested_time:
            return False
        if self.passengers.count() >= self.driver.available_seats:
            return False
        return True

    def add_passenger(self, passenger):
        if self.is_available_for_passenger(passenger, self.departure_time):
            self.passengers.add(passenger)
            self.save()

# Community Hub models
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.username} at {self.timestamp}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} at {self.timestamp}"

# Temporary Group Chat for Rides
class RideGroupChat(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='group_chats')
    passengers = models.ManyToManyField(Passenger)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Group Chat for Ride {self.ride.id} with Driver {self.driver.user.username}"

# Payment model
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_charge_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} by {self.user.username} for Ride {self.ride.id}"
