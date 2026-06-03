from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.orders.models import Order
from apps.products.models import Pizza


ROLES = ["Manager", "Kitchen", "Delivery", "Staff", "IT_Admin"]


class RoleService:

    @staticmethod
    def setup_roles():
        manager_group, _ = Group.objects.get_or_create(name="Manager")
        kitchen_group, _ = Group.objects.get_or_create(name="Kitchen")
        delivery_group, _ = Group.objects.get_or_create(name="Delivery")
        staff_group, _ = Group.objects.get_or_create(name="Staff")
        it_group, _ = Group.objects.get_or_create(name="IT_Admin")

        order_ct = ContentType.objects.get_for_model(Order)
        order_permissions = Permission.objects.filter(content_type=order_ct)
        manager_group.permissions.set(order_permissions)

        pizza_ct = ContentType.objects.get_for_model(Pizza)
        pizza_permissions = Permission.objects.filter(content_type=pizza_ct)
        staff_group.permissions.set(pizza_permissions)
