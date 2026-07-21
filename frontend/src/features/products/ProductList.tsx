import { useEffect, useReducer } from "react";
import type { Pizza, Category, PizzaSize } from "@/types";
import { productsApi } from "./productsApi";
import { ProductCard } from "./ProductCard";
import { LoadingState, ErrorState, EmptyState } from "@/components/state";
import { toUserMessage } from "@/services/api/apiErrors";
import styles from "./ProductList.module.css";

type State =
  | { status: "loading"; pizzas: Pizza[]; categories: Category[]; sizes: PizzaSize[]; selectedCategory: number | null }
  | { status: "error"; message: string; pizzas: Pizza[]; categories: Category[]; sizes: PizzaSize[]; selectedCategory: number | null }
  | { status: "ready"; pizzas: Pizza[]; categories: Category[]; sizes: PizzaSize[]; selectedCategory: number | null };

type Action =
  | { type: "LOAD_START" }
  | { type: "LOAD_DONE"; pizzas: Pizza[] }
  | { type: "LOAD_ERROR"; message: string }
  | { type: "META_LOADED"; categories: Category[]; sizes: PizzaSize[] }
  | { type: "SELECT_CATEGORY"; id: number | null };

const initial: State = {
  status: "loading",
  pizzas: [],
  categories: [],
  sizes: [],
  selectedCategory: null,
};

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "LOAD_START": return { ...state, status: "loading" };
    case "LOAD_DONE": return { ...state, status: "ready", pizzas: action.pizzas };
    case "LOAD_ERROR": return { ...state, status: "error", message: action.message };
    case "META_LOADED": return { ...state, categories: action.categories, sizes: action.sizes };
    case "SELECT_CATEGORY": return { ...state, selectedCategory: action.id };
    default: return state;
  }
}

export function ProductList() {
  const [state, dispatch] = useReducer(reducer, initial);

  useEffect(() => {
    Promise.all([productsApi.getCategories(), productsApi.getSizes()])
      .then(([cats, szs]) =>
        dispatch({ type: "META_LOADED", categories: cats.results, sizes: szs.results }),
      )
      .catch(() => {});
  }, []);

  useEffect(() => {
    let cancelled = false;
    dispatch({ type: "LOAD_START" });
    const params = state.selectedCategory !== null ? { category: state.selectedCategory } : undefined;

    productsApi
      .getPizzas(params)
      .then((data) => { if (!cancelled) dispatch({ type: "LOAD_DONE", pizzas: data.results }); })
      .catch((err: unknown) => { if (!cancelled) dispatch({ type: "LOAD_ERROR", message: toUserMessage(err) }); });

    return () => { cancelled = true; };
  }, [state.selectedCategory]);

  if (state.status === "loading" && state.pizzas.length === 0)
    return <LoadingState message="Caricamento menu..." />;
  if (state.status === "error")
    return <ErrorState message={state.message} onRetry={() => dispatch({ type: "SELECT_CATEGORY", id: state.selectedCategory })} />;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.titleGroup}>
          <span className={styles.eyebrow}>La nostra selezione</span>
          <h1 className={styles.title}>Il menu</h1>
        </div>
        <div className={styles.filters}>
          <button
            className={`${styles.filterBtn} ${state.selectedCategory === null ? styles.active : ""}`}
            onClick={() => dispatch({ type: "SELECT_CATEGORY", id: null })}
          >Tutte</button>
          {state.categories.map((cat) => (
            <button
              key={cat.id}
              className={`${styles.filterBtn} ${state.selectedCategory === cat.id ? styles.active : ""}`}
              onClick={() => dispatch({ type: "SELECT_CATEGORY", id: cat.id })}
            >{cat.name}</button>
          ))}
        </div>
      </div>

      {state.pizzas.length === 0 ? (
        <EmptyState title="Nessuna pizza trovata" description="Prova un'altra categoria." />
      ) : (
        <div className={styles.grid}>
          {state.pizzas.map((pizza) => (
            <ProductCard key={pizza.id} pizza={pizza} sizes={state.sizes} />
          ))}
        </div>
      )}
    </div>
  );
}
