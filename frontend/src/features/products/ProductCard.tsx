import { useState } from "react";
import type { Pizza, PizzaSize } from "@/types";
import { useCart } from "@/features/cart";
import styles from "./ProductCard.module.css";

interface Props {
  pizza: Pizza;
  sizes: PizzaSize[];
}

export function ProductCard({ pizza, sizes }: Props) {
  const { addItem } = useCart();
  const [selectedSize, setSelectedSize] = useState<PizzaSize | null>(
    sizes.length > 0 ? sizes[0] : null,
  );
  const [added, setAdded] = useState(false);

  const price = selectedSize
    ? (parseFloat(pizza.base_price) * parseFloat(selectedSize.price_multiplier)).toFixed(2)
    : pizza.base_price;

  function handleAdd() {
    if (!selectedSize) return;
    addItem(pizza, selectedSize);
    setAdded(true);
    setTimeout(() => setAdded(false), 1500);
  }

  return (
    <article className={styles.card}>
      <div className={styles.imageWrap}>
        {pizza.image ? (
          <img src={pizza.image} alt={pizza.name} className={styles.image} />
        ) : (
          <div className={styles.imagePlaceholder}>🍕</div>
        )}
        {pizza.is_featured && <span className={styles.featuredBadge}>⭐ In evidenza</span>}
      </div>

      <div className={styles.body}>
        <h3 className={styles.name}>{pizza.name}</h3>
        <p className={styles.description}>
          {pizza.short_description || pizza.description}
        </p>

        {sizes.length > 0 && (
          <div className={styles.sizes}>
            {sizes.map((s) => (
              <button
                key={s.id}
                className={`${styles.sizeBtn} ${selectedSize?.id === s.id ? styles.selected : ""}`}
                onClick={() => setSelectedSize(s)}
              >
                {s.name}
              </button>
            ))}
          </div>
        )}

        <div className={styles.footer}>
          <span className={styles.price}>€ {price}</span>
          {added ? (
            <span className={styles.addedFeedback}>✓ Aggiunto!</span>
          ) : (
            <button
              className={styles.addBtn}
              onClick={handleAdd}
              disabled={!selectedSize}
            >
              + Aggiungi
            </button>
          )}
        </div>
      </div>
    </article>
  );
}
