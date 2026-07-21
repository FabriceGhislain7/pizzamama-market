from apps.analytics.queries.sales_queries import SalesQueries


class DashboardService:

    @staticmethod
    def manager_dashboard():
        sales = SalesQueries.today_sales()
        top_products = SalesQueries.top_selling_products()
        weekly = SalesQueries.weekly_trend()

        return {
            "today": {
                "total_revenue": str(sales.get("total_revenue") or 0),
                "total_orders": sales.get("total_orders") or 0,
                "avg_order_value": str(sales.get("avg_order_value") or 0),
            },
            "top_products": top_products,
            "weekly_trend": [
                {
                    "day": entry["day"].isoformat() if entry.get("day") else None,
                    "total": str(entry.get("total") or 0),
                    "orders": entry.get("orders") or 0,
                }
                for entry in weekly
            ],
        }
