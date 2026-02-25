from rest_framework.routers import DefaultRouter
from .views import PizzaViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"pizzas", PizzaViewSet, basename="pizzas")

urlpatterns = router.urls