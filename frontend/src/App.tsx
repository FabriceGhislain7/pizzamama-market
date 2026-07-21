import { CartProvider } from "@/features/cart";
import { AuthProvider } from "@/features/auth";
import { AppRouter } from "@/app/router";

export function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <AppRouter />
      </CartProvider>
    </AuthProvider>
  );
}

export default App;
