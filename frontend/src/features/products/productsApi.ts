import { httpClient } from "@/services/api/httpClient";
import type { Pizza, Category, PizzaSize } from "@/types";
import type { PaginatedResponse } from "@/types";

export const productsApi = {
  getPizzas: (params?: { category?: number; search?: string }) => {
    const query = new URLSearchParams();
    if (params?.category) query.set("category", String(params.category));
    if (params?.search) query.set("search", params.search);
    const qs = query.toString();
    return httpClient.get<PaginatedResponse<Pizza>>(
      `/products/pizzas/${qs ? `?${qs}` : ""}`,
      { skipAuth: true },
    );
  },

  getCategories: () =>
    httpClient.get<PaginatedResponse<Category>>("/products/categories/", {
      skipAuth: true,
    }),

  getSizes: () =>
    httpClient.get<PaginatedResponse<PizzaSize>>("/products/sizes/", {
      skipAuth: true,
    }),
};
