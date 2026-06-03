import { NavLink } from "react-router-dom";
import styles from "./Header.module.css";

export function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.brand}>
        <NavLink to="/">🍕 PizzaMama</NavLink>
      </div>
      <nav className={styles.nav}>
        <NavLink to="/menu" className={({ isActive }) => (isActive ? styles.active : "")}>
          Menu
        </NavLink>
        <NavLink to="/cart" className={({ isActive }) => (isActive ? styles.active : "")}>
          Carrello
        </NavLink>
      </nav>
    </header>
  );
}
