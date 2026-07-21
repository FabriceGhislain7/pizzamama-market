import { httpClient } from "@/services/api/httpClient";

interface TodaySales {
  total_revenue: string;
  total_orders: number;
  avg_order_value: string;
}

interface TopProduct {
  pizza__name: string;
  total_sold: number;
}

interface WeeklyEntry {
  day: string | null;
  total: string;
  orders: number;
}

export interface DashboardData {
  today: TodaySales;
  top_products: TopProduct[];
  weekly_trend: WeeklyEntry[];
}

export const dashboardApi = {
  getDashboard: () => httpClient.get<DashboardData>("/analytics/dashboard/"),
};
