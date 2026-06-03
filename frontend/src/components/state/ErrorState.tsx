import { Button } from "@/components/ui/Button";
import styles from "./States.module.css";

interface ErrorStateProps {
  message?: string;
  onRetry?: () => void;
}

export function ErrorState({
  message = "Si è verificato un errore. Riprova.",
  onRetry,
}: ErrorStateProps) {
  return (
    <div className={styles.container} role="alert">
      <p className={styles.errorIcon}>⚠️</p>
      <p>{message}</p>
      {onRetry && (
        <Button variant="secondary" size="sm" onClick={onRetry}>
          Riprova
        </Button>
      )}
    </div>
  );
}
