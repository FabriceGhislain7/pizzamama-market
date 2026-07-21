import { NavLink, Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/features/auth";
import { useCart } from "@/features/cart";
import styles from "./Header.module.css";

export function Header() {
  const { isAuthenticated, user, logout } = useAuth();
  const { totalItems } = useCart();
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate("/login");
  }

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `${styles.navLink} ${isActive ? styles.active : ""}`;

  return (
    <header className={styles.header}>
      <div className={styles.inner}>
        <div className={styles.brand}>
          <Link to="/">
            <span className={styles.logo}>🍕</span>
            <div>
              <div className={styles.brandName}>PizzaMama</div>
              <div className={styles.brandSub}>Market</div>
            </div>
          </Link>
        </div>

        <nav className={styles.nav}>
          <NavLink to="/menu" className={linkClass}>Menu</NavLink>

          {isAuthenticated && (
            <NavLink to="/orders" className={linkClass}>I miei ordini</NavLink>
          )}

          <div className={styles.divider} />

          <NavLink to="/cart" className={styles.cartBtn}>
            🛒
            {totalItems > 0 && (
              <span className={styles.cartBadge}>{totalItems > 9 ? "9+" : totalItems}</span>
            )}
          </NavLink>

          {isAuthenticated ? (
            <>
              <NavLink to="/profile" className={styles.userChip}>
                {user?.username}
              </NavLink>
              <button className={styles.logoutBtn} onClick={() => void handleLogout()}>
                Esci
              </button>
            </>
          ) : (
            <NavLink to="/login" className={linkClass}>Accedi</NavLink>
          )}
        </nav>
      </div>
    </header>
  );
}
