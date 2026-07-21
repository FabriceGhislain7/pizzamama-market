import { Link } from "react-router-dom";
import { useReducer, useEffect } from "react";
import { productsApi } from "@/features/products";
import { ProductCard } from "@/features/products";
import type { Pizza, PizzaSize } from "@/types";
import { toUserMessage } from "@/services/api/apiErrors";
import { LoadingState, ErrorState } from "@/components/state";
import styles from "./HomePage.module.css";

type FeaturedState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; pizzas: Pizza[]; sizes: PizzaSize[] };

type FeaturedAction =
  | { type: "START" }
  | { type: "DONE"; pizzas: Pizza[]; sizes: PizzaSize[] }
  | { type: "ERROR"; message: string };

function featuredReducer(_: FeaturedState, action: FeaturedAction): FeaturedState {
  if (action.type === "START") return { status: "loading" };
  if (action.type === "DONE") return { status: "ready", pizzas: action.pizzas, sizes: action.sizes };
  if (action.type === "ERROR") return { status: "error", message: action.message };
  return { status: "loading" };
}

function FeaturedProducts() {
  const [state, dispatch] = useReducer(featuredReducer, { status: "loading" });

  useEffect(() => {
    let cancelled = false;
    dispatch({ type: "START" });
    Promise.all([
      productsApi.getPizzas(),
      productsApi.getSizes(),
    ])
      .then(([pizzasData, sizesData]) => {
        if (!cancelled) {
          const featured = pizzasData.results.filter((p) => p.is_featured).slice(0, 3);
          const all = featured.length >= 3 ? featured : pizzasData.results.slice(0, 3);
          dispatch({ type: "DONE", pizzas: all, sizes: sizesData.results });
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) dispatch({ type: "ERROR", message: toUserMessage(err) });
      });
    return () => { cancelled = true; };
  }, []);

  if (state.status === "loading") return <LoadingState message="Caricamento..." />;
  if (state.status === "error") return <ErrorState message={state.message} />;

  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: "var(--space-5)" }}>
      {state.pizzas.map((pizza) => (
        <ProductCard key={pizza.id} pizza={pizza} sizes={state.sizes} />
      ))}
    </div>
  );
}

export function HomePage() {
  return (
    <>
      {/* HERO */}
      <section className={styles.hero}>
        <div className={styles.heroInner}>
          <div className={styles.heroContent}>
            <span className={styles.heroEyebrow}>🔥 Ordina ora, pronto in 25 minuti</span>
            <h1 className={styles.heroTitle}>
              La pizza<br />
              <span>artigianale</span><br />
              a casa tua
            </h1>
            <p className={styles.heroSubtitle}>
              Ingredienti freschi ogni giorno, impasto a lunga lievitazione e sapori autentici.
              Scegli dalla nostra selezione di pizze classiche e speciali.
            </p>
            <div className={styles.heroActions}>
              <Link to="/menu" className={styles.btnPrimary}>
                🍕 Sfoglia il menu
              </Link>
              <Link to="/register" className={styles.btnSecondary}>
                Crea account
              </Link>
            </div>
            <div className={styles.heroStats}>
              <div className={styles.stat}>
                <span className={styles.statNum}>25'</span>
                <span className={styles.statLabel}>Consegna media</span>
              </div>
              <div className={styles.stat}>
                <span className={styles.statNum}>30+</span>
                <span className={styles.statLabel}>Varietà di pizza</span>
              </div>
              <div className={styles.stat}>
                <span className={styles.statNum}>4.8★</span>
                <span className={styles.statLabel}>Valutazione media</span>
              </div>
            </div>
          </div>
          <div className={styles.heroVisual}>🍕</div>
        </div>
      </section>

      {/* STRIP */}
      <div className={styles.strip}>
        <div className={styles.stripInner}>
          <div className={styles.stripItem}><span>🚀</span> Consegna in 25 minuti</div>
          <div className={styles.stripItem}><span>🌾</span> Ingredienti freschi ogni giorno</div>
          <div className={styles.stripItem}><span>👨‍🍳</span> Pizzaioli esperti</div>
          <div className={styles.stripItem}><span>♻️</span> Packaging eco-sostenibile</div>
        </div>
      </div>

      {/* PIZZE IN EVIDENZA */}
      <section className={styles.featured}>
        <div className={styles.featuredInner}>
          <div className={styles.featuredHeader}>
            <div>
              <p className={styles.sectionEyebrow}>Le più amate</p>
              <h2 className={styles.sectionTitle}>Pizze in evidenza</h2>
            </div>
            <Link to="/menu" className={styles.seeAll}>Vedi tutto il menu →</Link>
          </div>
          <FeaturedProducts />
        </div>
      </section>

      {/* FEATURES */}
      <section className={styles.features}>
        <div className={styles.featuresInner}>
          <div className={styles.sectionHeader}>
            <p className={styles.sectionEyebrow}>Perché sceglierci</p>
            <h2 className={styles.sectionTitle}>Qualità in ogni morso</h2>
          </div>
          <div className={styles.grid3}>
            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>🌾</div>
              <h3>Ingredienti selezionati</h3>
              <p>Farina tipo 00, mozzarella fior di latte, pomodori San Marzano DOP.
                Solo il meglio, senza compromessi.</p>
            </div>
            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>⏰</div>
              <h3>Lievitazione lenta</h3>
              <p>Il nostro impasto riposa 48 ore per essere leggero e digeribile.
                Niente fretta, niente scorciatoie.</p>
            </div>
            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>🔥</div>
              <h3>Forno a legna</h3>
              <p>Cotta a 450°C per 90 secondi. Bordo croccante, centro morbido.
                Esattamente come a Napoli.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className={styles.cta}>
        <div className={styles.ctaInner}>
          <p style={{ fontSize: "3rem" }}>🍕</p>
          <h2 className={styles.ctaTitle}>Pronto a ordinare?</h2>
          <p className={styles.ctaSubtitle}>
            Crea il tuo account in 30 secondi e ricevi la tua pizza in meno di mezz'ora.
          </p>
          <Link to="/menu" className={styles.btnWhite}>
            Ordina ora
          </Link>
        </div>
      </section>
    </>
  );
}
