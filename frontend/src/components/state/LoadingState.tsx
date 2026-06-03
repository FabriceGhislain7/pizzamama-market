import styles from "./States.module.css";

interface LoadingStateProps {
  message?: string;
}

export function LoadingState({ message = "Caricamento..." }: LoadingStateProps) {
  return (
    <div className={styles.container} role="status" aria-live="polite">
      <div className={styles.spinner} aria-hidden="true" />
      <p>{message}</p>
    </div>
  );
}
