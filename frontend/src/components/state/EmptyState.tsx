import styles from "./States.module.css";

interface EmptyStateProps {
  title?: string;
  description?: string;
  action?: React.ReactNode;
}

export function EmptyState({
  title = "Nessun risultato",
  description,
  action,
}: EmptyStateProps) {
  return (
    <div className={styles.container}>
      <p className={styles.emptyIcon}>📭</p>
      <h3>{title}</h3>
      {description && <p className={styles.description}>{description}</p>}
      {action}
    </div>
  );
}
