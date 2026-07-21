import { useReducer, useEffect, useRef } from "react";

type State<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; message: string };

type Action<T> =
  | { type: "START" }
  | { type: "SUCCESS"; data: T }
  | { type: "ERROR"; message: string }
  | { type: "RESET" };

function reducer<T>(state: State<T>, action: Action<T>): State<T> {
  switch (action.type) {
    case "START": return { status: "loading" };
    case "SUCCESS": return { status: "success", data: action.data };
    case "ERROR": return { status: "error", message: action.message };
    case "RESET": return { status: "idle" };
    default: return state;
  }
}

export function useAsync<T>(fn: () => Promise<T>, deps: unknown[] = []) {
  const [state, dispatch] = useReducer(reducer<T>, { status: "loading" });
  const cancelledRef = useRef(false);

  useEffect(() => {
    cancelledRef.current = false;
    dispatch({ type: "START" });

    fn()
      .then((data) => {
        if (!cancelledRef.current) dispatch({ type: "SUCCESS", data });
      })
      .catch((err: unknown) => {
        if (!cancelledRef.current) {
          const msg = err instanceof Error ? err.message : "Errore sconosciuto";
          dispatch({ type: "ERROR", message: msg });
        }
      });

    return () => {
      cancelledRef.current = true;
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  const reset = () => dispatch({ type: "RESET" });
  return { state, reset };
}
