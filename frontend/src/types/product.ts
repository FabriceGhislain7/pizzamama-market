export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
}

export interface Allergen {
  id: number;
  name: string;
  symbol: string;
}

export interface Ingredient {
  id: number;
  name: string;
  price_per_extra: string;
  is_active: boolean;
}

export interface PizzaSize {
  id: number;
  name: string;
  diameter_cm: number;
  price_multiplier: string;
}

export interface Pizza {
  id: number;
  name: string;
  slug: string;
  description: string;
  short_description: string;
  base_price: string;
  category: Category;
  image: string | null;
  is_active: boolean;
  is_featured: boolean;
}
