import { Link } from "react-router-dom";
import styles from "./Footer.module.css";

export function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.inner}>
        <div className={styles.brand}>
          <div className={styles.brandName}>🍕 PizzaMama Market</div>
          <p className={styles.brandTagline}>
            Le migliori pizze artigianali, ingredienti freschi e impasto tradizionale.
            Consegna a domicilio o ritiro in sede — ogni giorno dalle 11:30 alle 23:00.
          </p>
          <div className={styles.contacts}>
            <span className={styles.contact}>📍 Via Roma 42, Milano</span>
            <span className={styles.contact}>📞 02 1234 5678</span>
            <span className={styles.contact}>✉️ info@pizzamama.it</span>
          </div>
        </div>

        <div className={styles.col}>
          <h4>Menu</h4>
          <ul>
            <li><Link to="/menu">Tutte le pizze</Link></li>
            <li><Link to="/menu">Classiche</Link></li>
            <li><Link to="/menu">Speciali</Link></li>
            <li><Link to="/menu">Senza glutine</Link></li>
          </ul>
        </div>

        <div className={styles.col}>
          <h4>Account</h4>
          <ul>
            <li><Link to="/login">Accedi</Link></li>
            <li><Link to="/register">Registrati</Link></li>
            <li><Link to="/orders">I miei ordini</Link></li>
            <li><Link to="/profile">Profilo</Link></li>
          </ul>
        </div>

        <div className={styles.col}>
          <h4>Info</h4>
          <ul>
            <li><Link to="/">Chi siamo</Link></li>
            <li><Link to="/">Allergeni</Link></li>
            <li><Link to="/">Privacy policy</Link></li>
            <li><Link to="/">Termini di servizio</Link></li>
          </ul>
        </div>
      </div>

      <div className={styles.bottom}>
        <span>© {new Date().getFullYear()} PizzaMama Market. Tutti i diritti riservati.</span>
        <span>P.IVA 12345678901 · Milano</span>
      </div>
    </footer>
  );
}
