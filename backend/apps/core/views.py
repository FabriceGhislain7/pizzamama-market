from django.db import connection
from django.http import JsonResponse


def health_check(request):
    response_status = 200

    try:
        connection.ensure_connection()
        database_status = "ok"
    except Exception:
        response_status = 503
        database_status = "error"

    return JsonResponse(
        {
            "status": "ok" if database_status == "ok" else "error",
            "database": database_status,
        },
        status=response_status,
    )
