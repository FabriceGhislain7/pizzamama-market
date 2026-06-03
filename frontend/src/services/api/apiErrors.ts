export class ApiError extends Error {
  declare status: number;
  declare detail: unknown;

  constructor(status: number, message: string, detail?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

const USER_MESSAGES: Record<number, string> = {
  400: "Dati non validi. Controlla i campi e riprova.",
  401: "Sessione scaduta. Effettua di nuovo il login.",
  403: "Non hai i permessi per questa operazione.",
  404: "Risorsa non trovata.",
  429: "Troppe richieste. Attendi qualche momento.",
  500: "Errore del server. Riprova tra poco.",
};

export function toUserMessage(error: unknown): string {
  if (error instanceof ApiError) {
    return USER_MESSAGES[error.status] ?? "Si è verificato un errore. Riprova.";
  }
  if (error instanceof Error && error.message === "Failed to fetch") {
    return "Impossibile raggiungere il server. Controlla la connessione.";
  }
  return "Si è verificato un errore imprevisto.";
}
