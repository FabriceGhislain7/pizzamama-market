import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { ProtectedRoute } from "./ProtectedRoute";
import { StaffRoute } from "./StaffRoute";
import { HomePage } from "@/pages/HomePage";
import { MenuPage } from "@/pages/MenuPage";
import { CartPage } from "@/pages/CartPage";
import { NotFoundPage } from "@/pages/NotFoundPage";
import { LoginPage, RegisterPage } from "@/features/auth";
import { CheckoutPage } from "@/features/checkout";
import { OrdersPage } from "@/features/orders";
import { ProfilePage } from "@/features/account";
import { StaffOrdersPage } from "@/features/staff";
import { DashboardPage } from "@/features/dashboard";

const router = createBrowserRouter([
  { path: "/login", element: <LoginPage /> },
  { path: "/register", element: <RegisterPage /> },

  {
    path: "/",
    element: <AppLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: "menu", element: <MenuPage /> },
      {
        path: "cart",
        element: <ProtectedRoute><CartPage /></ProtectedRoute>,
      },
      {
        path: "checkout",
        element: <ProtectedRoute><CheckoutPage /></ProtectedRoute>,
      },
      {
        path: "orders",
        element: <ProtectedRoute><OrdersPage /></ProtectedRoute>,
      },
      {
        path: "profile",
        element: <ProtectedRoute><ProfilePage /></ProtectedRoute>,
      },
      {
        path: "staff",
        element: <StaffRoute><StaffOrdersPage /></StaffRoute>,
      },
      {
        path: "dashboard",
        element: <StaffRoute><DashboardPage /></StaffRoute>,
      },
    ],
  },
  { path: "*", element: <NotFoundPage /> },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
