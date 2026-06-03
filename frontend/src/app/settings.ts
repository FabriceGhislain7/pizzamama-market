const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

if (!apiBaseUrl) {
  throw new Error("VITE_API_BASE_URL is not defined. Check your .env.local file.");
}

export const settings = {
  apiBaseUrl,
} as const;
