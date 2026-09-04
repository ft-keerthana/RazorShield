import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export async function getDashboardSummary() {
  const response = await api.get("/dashboard/summary");
  return response.data;
}

export async function getRecentTransactions(limit = 8) {
  const response = await api.get(
    `/transactions/recent?limit=${limit}`
  );
  return response.data;
}

export async function getTransactionInvestigation(transactionId) {
  const response = await api.get(
    `/transactions/${transactionId}`
  );
  return response.data;
}

export async function scoreTransaction(transactionId) {
  const response = await api.post(
    `/transactions/${transactionId}/score`
  );
  return response.data;
}