import { CartProvider } from "@/features/cart";
import { AppRouter } from "@/app/router";

export function App() {
  return (
    <CartProvider>
      <AppRouter />
    </CartProvider>
  );
}

export default App;
