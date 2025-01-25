#admin.py
from django.contrib import admin
from .models import User, Driver, Passenger, Ride, Post, Comment, RideGroupChat

# Register the custom User model
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'is_driver', 'is_passenger', 'date_joined')
    search_fields = ('username', 'phone_number')

admin.site.register(User, UserAdmin)

# Register the Driver model
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'vehicle_details', 'available_seats', 'is_available')
    search_fields = ('user__username', 'license_number')
    list_filter = ('is_available',)

admin.site.register(Driver, DriverAdmin)

# Register the Passenger model
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('user', 'emergency_contact', 'live_location_sharing')
    search_fields = ('user__username', 'emergency_contact')

admin.site.register(Passenger, PassengerAdmin)

# Register the Ride model
class RideAdmin(admin.ModelAdmin):
    list_display = ('driver', 'pickup_location', 'dropoff_location', 'distance', 'price_per_head', 'departure_time', 'ride_status')
    search_fields = ('driver__user__username', 'pickup_location', 'dropoff_location')
    list_filter = ('ride_status', 'departure_time')

admin.site.register(Ride, RideAdmin)

# Register the Post model
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'timestamp')
    search_fields = ('author__username', 'content')

admin.site.register(Post, PostAdmin)

# Register the Comment model
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'timestamp')
    search_fields = ('author__username', 'content')

admin.site.register(Comment, CommentAdmin)

# Register the RideGroupChat model
class RideGroupChatAdmin(admin.ModelAdmin):
    list_display = ('ride', 'driver', 'message', 'timestamp')
    search_fields = ('ride__id', 'driver__user__username', 'message')

admin.site.register(RideGroupChat, RideGroupChatAdmin)

