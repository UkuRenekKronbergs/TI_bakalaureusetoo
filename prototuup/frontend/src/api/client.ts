import type { AnalyysiPaaring, AnalyysiVastus } from "../types";

const API_BASE = import.meta.env.VITE_API_URL ?? "";

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function jsonOrThrow<T>(vastus: Response): Promise<T> {
  if (!vastus.ok) {
    let detail = vastus.statusText;
    try {
      const keha = await vastus.json();
      detail = keha.detail ?? detail;
    } catch {
      // mitte-JSON keha
    }
    throw new ApiError(vastus.status, detail);
  }
  return (await vastus.json()) as T;
}

export async function analyysi(paaring: AnalyysiPaaring): Promise<AnalyysiVastus> {
  const vastus = await fetch(`${API_BASE}/api/analyse`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(paaring),
  });
  return jsonOrThrow<AnalyysiVastus>(vastus);
}

export async function tervis(): Promise<{ olek: string }> {
  const vastus = await fetch(`${API_BASE}/api/health`);
  return jsonOrThrow(vastus);
}
