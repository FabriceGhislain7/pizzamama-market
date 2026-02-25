from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Address


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline, AddressInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "loyalty_points", "total_orders")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "label", "city", "is_default")
    list_filter = ("city", "is_default")