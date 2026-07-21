class PrivacyService:

    @staticmethod
    def export_user_data(user):
        addresses = list(
            user.addresses.values(
                "id", "label", "street_address", "city", "postal_code", "country", "is_default"
            )
        )
        orders = list(
            user.orders.values(
                "id", "order_number", "order_type", "status",
                "subtotal", "total_amount", "created_at",
            )
        )
        return {
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "date_joined": user.date_joined.isoformat() if user.date_joined else None,
            },
            "addresses": addresses,
            "orders": orders,
        }
