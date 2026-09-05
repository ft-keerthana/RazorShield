import axios from "axios";

const api = axios.create({
  baseURL:import.meta.env.VITE_API_URL,
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

export async function getFraudTrend(days = 7) {
  const response = await api.get(`/dashboard/fraud-trend?days=${days}`);
  return response.data;
}
export async function getNetworkOverview() {
  const response = await api.get("/network/overview");
  return response.data;
}

export async function getSuspiciousDevices(limit = 10) {
  const response = await api.get(
    `/network/suspicious-devices?limit=${limit}`
  );
  return response.data;
}

export async function getSuspiciousIPs(limit = 10) {
  const response = await api.get(
    `/network/suspicious-ips?limit=${limit}`
  );
  return response.data;
}

export async function getEvaluationMetrics() {
  const response = await api.get("/evaluation/metrics");
  return response.data;
}