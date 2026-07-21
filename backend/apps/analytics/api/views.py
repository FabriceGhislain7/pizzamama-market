from rest_framework.views import APIView
from rest_framework.response import Response
from apps.core.permissions import IsManager, IsITAdmin


class ManagerDashboardView(APIView):
    permission_classes = [IsManager | IsITAdmin]

    def get(self, request):
        from apps.analytics.services.dashboard_service import DashboardService
        data = DashboardService.manager_dashboard()
        return Response(data)
