from django.db import connection
from django.http import JsonResponse


def health_check(request):
    try:
        connection.ensure_connection()
        database_status = "ok"
    except Exception:
        database_status = "error"

    return JsonResponse(
        {
            "status": "ok",
            "database": database_status,
        }
    )
