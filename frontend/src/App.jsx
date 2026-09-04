import { useEffect, useState } from "react";

import {
  Activity,
  AlertTriangle,
  BarChart3,
  Bell,
  ChevronDown,
  CreditCard,
  GitBranch,
  LayoutDashboard,
  Network,
  Search,
  Settings,
  Shield,
  ShieldCheck,
  Users,
  X,
  Clock3,
  MapPin,
  Smartphone,
  Globe,
  AlertCircle,
} from "lucide-react";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import "./index.css";

import {
  getDashboardSummary,
  getRecentTransactions,
  getTransactionInvestigation,
} from "./services/api";


// ---------------------------------------------------------
// Demo trend data
// ---------------------------------------------------------

const fraudTrend = [
  { day: "Aug 28", rate: 1.8 },
  { day: "Aug 29", rate: 2.7 },
  { day: "Aug 30", rate: 2.0 },
  { day: "Aug 31", rate: 3.4 },
  { day: "Sep 1", rate: 3.0 },
  { day: "Sep 2", rate: 4.0 },
  { day: "Sep 3", rate: 2.6 },
  { day: "Sep 4", rate: 2.9 },
];


// ---------------------------------------------------------
// Sidebar
// ---------------------------------------------------------

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">
          <ShieldCheck size={25} />
        </div>

        <div>
          <div className="brand-name">RAZORSENTRY</div>
          <div className="brand-subtitle">Risk Intelligence</div>
        </div>
      </div>

      <nav className="nav">
        <div className="nav-section-title">OVERVIEW</div>

        <a className="nav-item active">
          <LayoutDashboard size={19} />
          <span>Dashboard</span>
        </a>

        <a className="nav-item">
          <CreditCard size={19} />
          <span>Transactions</span>
        </a>

        <a className="nav-item">
          <Search size={19} />
          <span>Investigation</span>
        </a>

        <div className="nav-section-title">INTELLIGENCE</div>

        <a className="nav-item">
          <Network size={19} />
          <span>Network Intelligence</span>
        </a>

        <a className="nav-item">
          <Shield size={19} />
          <span>Rules & Policies</span>
        </a>

        <a className="nav-item">
          <Bell size={19} />
          <span>Alerts</span>
          <span className="nav-badge">5</span>
        </a>

        <a className="nav-item">
          <BarChart3 size={19} />
          <span>Reports</span>
        </a>

        <div className="nav-section-title">SYSTEM</div>

        <a className="nav-item">
          <Settings size={19} />
          <span>Settings</span>
        </a>
      </nav>

      <div className="system-status">
        <div className="status-heading">SYSTEM STATUS</div>

        <div className="status-row">
          <span className="status-dot" />
          <span>All systems operational</span>
        </div>
      </div>
    </aside>
  );
}


// ---------------------------------------------------------
// Header
// ---------------------------------------------------------

function Header() {
  return (
    <header className="header">
      <div>
        <h1>Dashboard</h1>
        <p>Real-time payment risk intelligence overview</p>
      </div>

      <div className="header-actions">
        <button className="date-button">
          <Activity size={16} />
          Aug 28 – Sep 4, 2026
          <ChevronDown size={15} />
        </button>

        <button className="icon-button notification">
          <Bell size={18} />
          <span>3</span>
        </button>

        <div className="profile">
          <div className="avatar">K</div>

          <div>
            <strong>Keerthana</strong>
            <small>Admin</small>
          </div>

          <ChevronDown size={15} />
        </div>
      </div>
    </header>
  );
}


// ---------------------------------------------------------
// Stat Card
// ---------------------------------------------------------

function StatCard({
  icon,
  title,
  value,
  description,
  variant = "purple",
}) {
  return (
    <div className="stat-card">
      <div className={`stat-icon ${variant}`}>
        {icon}
      </div>

      <div className="stat-content">
        <span className="stat-title">{title}</span>
        <strong className="stat-value">{value}</strong>

        <span className={`stat-description ${variant}`}>
          {description}
        </span>
      </div>
    </div>
  );
}


// ---------------------------------------------------------
// Network Intelligence
// ---------------------------------------------------------

function NetworkIntelligence({ dashboardData }) {
  const networkRisk = dashboardData.network_risk_score;

  const networkRiskLabel =
    networkRisk >= 0.7
      ? "High network risk"
      : networkRisk >= 0.4
        ? "Medium network risk"
        : "Low network risk";

  return (
    <section className="card network-card">
      <div className="card-header">
        <div>
          <h2>Network Intelligence</h2>
          <p>Current network-level risk signals</p>
        </div>

        <button className="more-button">...</button>
      </div>

      <div className="network-list">

        <div className="network-item">
          <div className="network-icon purple">
            <Activity size={17} />
          </div>

          <div className="network-label">
            <strong>Fraud Spike</strong>
            <span>Recent fraud activity</span>
          </div>

          <span
            className={`network-status ${
              dashboardData.fraud_spike
                ? "warning"
                : "safe"
            }`}
          >
            {dashboardData.fraud_spike
              ? "Detected"
              : "No Spike"}
          </span>
        </div>


        <div className="network-item">
          <div className="network-icon purple">
            <GitBranch size={17} />
          </div>

          <div className="network-label">
            <strong>Abuse Network</strong>
            <span>Candidate network detection</span>
          </div>

          <span
            className={`network-status ${
              dashboardData.abuse_ring_detected
                ? "warning"
                : "safe"
            }`}
          >
            {dashboardData.abuse_ring_detected
              ? "Detected"
              : "None"}
          </span>
        </div>


        <div className="network-item">
          <div className="network-icon blue">
            <Users size={17} />
          </div>

          <div className="network-label">
            <strong>Network Risk</strong>
            <span>{networkRiskLabel}</span>
          </div>

          <strong className="network-number">
            {Math.round(networkRisk * 100)}
          </strong>
        </div>


        <div className="network-item">
          <div className="network-icon blue">
            <Network size={17} />
          </div>

          <div className="network-label">
            <strong>Network Status</strong>
            <span>Aggregated intelligence</span>
          </div>

          <strong className="network-number">
            Active
          </strong>
        </div>

      </div>

      <button className="primary-button">
        <Network size={16} />
        View Network Intelligence
      </button>
    </section>
  );
}


// ---------------------------------------------------------
// Risk Distribution
// ---------------------------------------------------------

function RiskDistribution({ dashboardData }) {
  const total = dashboardData.total_transactions;
  const fraud = dashboardData.fraud_transactions;
  const legitimate = dashboardData.legitimate_transactions;

  const fraudPercentage = total
    ? ((fraud / total) * 100).toFixed(1)
    : "0.0";

  const legitimatePercentage = total
    ? ((legitimate / total) * 100).toFixed(1)
    : "0.0";

  return (
    <section className="card distribution-card">
      <div className="card-header">
        <div>
          <h2>Transaction Outcome</h2>
          <p>Ground-truth dataset distribution</p>
        </div>
      </div>

      <div className="distribution">

        <div className="donut">
          <div className="donut-center">
            <strong>{total.toLocaleString()}</strong>
            <span>Total</span>
          </div>
        </div>

        <div className="legend">

          <div className="legend-item">
            <span className="legend-dot green" />

            <div>
              <strong>Legitimate</strong>
              <span>
                {legitimate.toLocaleString()} ·{" "}
                {legitimatePercentage}%
              </span>
            </div>
          </div>


          <div className="legend-item">
            <span className="legend-dot red" />

            <div>
              <strong>Fraud</strong>
              <span>
                {fraud.toLocaleString()} ·{" "}
                {fraudPercentage}%
              </span>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}


// ---------------------------------------------------------
// Investigation Panel
// ---------------------------------------------------------

function InvestigationPanel({
  transaction,
  loading,
  error,
  onClose,
}) {
  if (!transaction && !loading && !error) {
    return null;
  }

  return (
    <div className="investigation-overlay">
      <div className="investigation-panel">

        <div className="investigation-header">
          <div>
            <span className="investigation-eyebrow">
              TRANSACTION INVESTIGATION
            </span>

            <h2>
              {transaction?.transaction_id || "Loading..."}
            </h2>
          </div>

          <button
            className="investigation-close"
            onClick={onClose}
            aria-label="Close investigation"
          >
            <X size={19} />
          </button>
        </div>


        {loading && (
          <div className="investigation-loading">
            <div className="investigation-spinner" />
            Loading transaction intelligence...
          </div>
        )}


        {error && !loading && (
          <div className="investigation-error">
            <AlertCircle size={20} />
            <div>
              <strong>Investigation unavailable</strong>
              <span>{error}</span>
            </div>
          </div>
        )}


        {transaction && !loading && !error && (
          <div className="investigation-content">

            {/* Risk summary */}

            <div className="investigation-risk-card">
              <div>
                <span className="investigation-label">
                  RULE RISK SCORE
                </span>

                <strong
                  className={`investigation-score ${transaction.rule_risk_level}`}
                >
                  {Number(
                    transaction.rule_risk_score
                  ).toFixed(2)}
                </strong>

                <span
                  className={`investigation-risk-level ${transaction.rule_risk_level}`}
                >
                  {transaction.rule_risk_level?.toUpperCase()}
                </span>
              </div>

              <div className="investigation-ground-truth">
                <span>SCENARIO</span>
                <strong>
                  {transaction.scenario
                    ?.replaceAll("_", " ")
                    .toUpperCase()}
                </strong>
              </div>
            </div>


            {/* Transaction details */}

            <div className="investigation-section">
              <div className="investigation-section-title">
                <CreditCard size={16} />
                Transaction Details
              </div>

              <div className="investigation-detail-grid">

                <div className="investigation-detail">
                  <span>Amount</span>
                  <strong>
                    {transaction.currency}{" "}
                    {Number(transaction.amount).toFixed(2)}
                  </strong>
                </div>

                <div className="investigation-detail">
                  <span>Status</span>
                  <strong className="capitalize">
                    {transaction.status}
                  </strong>
                </div>

                <div className="investigation-detail">
                  <span>Customer</span>
                  <strong>
                    {transaction.customer_id}
                  </strong>
                </div>

                <div className="investigation-detail">
                  <span>Merchant</span>
                  <strong>
                    {transaction.merchant_id}
                  </strong>
                </div>

                <div className="investigation-detail">
                  <span>Timestamp</span>
                  <strong>
                    {new Date(
                      transaction.timestamp
                    ).toLocaleString()}
                  </strong>
                </div>

                <div className="investigation-detail">
                  <span>Scenario</span>
                  <strong className="capitalize">
                    {transaction.scenario?.replaceAll(
                      "_",
                      " "
                    )}
                  </strong>
                </div>

              </div>
            </div>


            {/* Risk reasons */}

            <div className="investigation-section">
              <div className="investigation-section-title">
                <AlertTriangle size={16} />
                Risk Signals
              </div>

              {transaction.risk_reasons?.length > 0 ? (
                <div className="risk-reason-list">
                  {transaction.risk_reasons.map(
                    (reason, index) => (
                      <div
                        className="risk-reason"
                        key={`${reason}-${index}`}
                      >
                        <span className="risk-reason-dot" />
                        <span>{reason}</span>
                      </div>
                    )
                  )}
                </div>
              ) : (
                <div className="no-risk-signals">
                  No rule-based risk signals detected.
                </div>
              )}
            </div>


            {/* Behavioral signals */}

            <div className="investigation-section">
              <div className="investigation-section-title">
                <Activity size={16} />
                Behavioral Signals
              </div>

              <div className="signal-grid">

                <div className="signal-card">
                  <Clock3 size={15} />
                  <span>Customer velocity · 5m</span>
                  <strong>
                    {transaction.customer_velocity_5m}
                  </strong>
                </div>

                <div className="signal-card">
                  <Clock3 size={15} />
                  <span>Customer velocity · 1h</span>
                  <strong>
                    {transaction.customer_velocity_1h}
                  </strong>
                </div>

                <div className="signal-card">
                  <Smartphone size={15} />
                  <span>Device velocity · 5m</span>
                  <strong>
                    {transaction.device_velocity_5m}
                  </strong>
                </div>

                <div className="signal-card">
                  <Globe size={15} />
                  <span>IP velocity · 5m</span>
                  <strong>
                    {transaction.ip_velocity_5m}
                  </strong>
                </div>

                <div className="signal-card">
                  <AlertTriangle size={15} />
                  <span>Failed attempts · 1h</span>
                  <strong>
                    {transaction.failed_attempts_1h}
                  </strong>
                </div>

                <div className="signal-card">
                  <Users size={15} />
                  <span>Shared device</span>
                  <strong>
                    {transaction.shared_device_flag
                      ? "Yes"
                      : "No"}
                  </strong>
                </div>

                <div className="signal-card">
                  <Network size={15} />
                  <span>Shared IP</span>
                  <strong>
                    {transaction.shared_ip_flag
                      ? "Yes"
                      : "No"}
                  </strong>
                </div>

              </div>
            </div>


            {/* Investigation note */}

            <div className="investigation-note">
              <ShieldCheck size={17} />

              <div>
                <strong>
                  Investigator view
                </strong>

                <span>
                  Signals shown here are derived from
                  RazorSentry's rule and behavioral
                  analysis pipeline. ML scoring and
                  policy decisions will be displayed
                  in the next stage.
                </span>
              </div>
            </div>

          </div>
        )}

      </div>
    </div>
  );
}


// ---------------------------------------------------------
// Recent Transactions
// ---------------------------------------------------------

function RecentTransactions({
  transactions,
  onSelectTransaction,
}) {
  return (
    <section className="card transactions-card">
      <div className="card-header">
        <div>
          <h2>Recent Transactions</h2>
          <p>Latest transactions evaluated by RazorSentry</p>
        </div>

        <button className="secondary-button">
          View All
        </button>
      </div>

      <div className="transaction-table-wrapper">
        <table>
          <thead>
            <tr>
              <th>TRANSACTION ID</th>
              <th>AMOUNT</th>
              <th>CUSTOMER</th>
              <th>RISK SCORE</th>
              <th>RISK LEVEL</th>
              <th>TIME</th>
            </tr>
          </thead>

          <tbody>
            {transactions.length === 0 ? (
              <tr>
                <td colSpan="6" className="time">
                  No recent transactions available.
                </td>
              </tr>
            ) : (
              transactions.map((transaction) => {
                const risk =
                  transaction.risk_level || "low";

                const score =
                  transaction.risk_score ?? 0;

                return (
                  <tr
                    key={transaction.transaction_id}
                    className="transaction-row"
                    onClick={() =>
                      onSelectTransaction(
                        transaction.transaction_id
                      )
                    }
                  >
                    <td>
                      <div className="transaction-id">
                        <span
                          className={`risk-dot ${risk}`}
                        />

                        {transaction.transaction_id}
                      </div>
                    </td>

                    <td className="amount">
                      {transaction.currency}{" "}
                      {Number(
                        transaction.amount
                      ).toFixed(2)}
                    </td>

                    <td className="customer">
                      {transaction.customer_id || "—"}
                    </td>

                    <td>
                      <span
                        className={`score ${risk}`}
                      >
                        {Number(score).toFixed(2)}
                      </span>
                    </td>

                    <td>
                      <span
                        className={`risk-level-badge ${risk}`}
                      >
                        {risk.toUpperCase()}
                      </span>
                    </td>

                    <td className="time">
                      {new Date(
                        transaction.timestamp
                      ).toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}


// ---------------------------------------------------------
// Dashboard
// ---------------------------------------------------------

function Dashboard() {
  const [dashboardData, setDashboardData] =
    useState(null);

  const [recentTransactions, setRecentTransactions] =
    useState([]);

  const [selectedTransaction, setSelectedTransaction] =
    useState(null);

  const [investigationLoading, setInvestigationLoading] =
    useState(false);

  const [investigationError, setInvestigationError] =
    useState("");


  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const [
          dashboardSummary,
          transactions,
        ] = await Promise.all([
          getDashboardSummary(),
          getRecentTransactions(),
        ]);

        setDashboardData(dashboardSummary);

        setRecentTransactions(
          transactions.map((transaction) => ({
            ...transaction,
            customer_id:
              transaction.customer_id || null,
          }))
        );

      } catch (err) {
        console.error(
          "Failed to load dashboard:",
          err
        );

        setError(
          "Unable to load live dashboard data."
        );
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, []);


  const handleSelectTransaction = async (
    transactionId
  ) => {
    setSelectedTransaction(null);
    setInvestigationError("");
    setInvestigationLoading(true);

    try {
      const investigation =
        await getTransactionInvestigation(
          transactionId
        );

      setSelectedTransaction(investigation);

    } catch (err) {
      console.error(
        "Failed to load investigation:",
        err
      );

      setInvestigationError(
        err.response?.data?.detail ||
        "Unable to load transaction investigation."
      );

    } finally {
      setInvestigationLoading(false);
    }
  };


  const closeInvestigation = () => {
    setSelectedTransaction(null);
    setInvestigationError("");
    setInvestigationLoading(false);
  };


  if (loading) {
    return (
      <div className="loading-screen">
        Loading RazorSentry...
      </div>
    );
  }


  if (error || !dashboardData) {
    return (
      <div className="loading-screen">
        {error || "Dashboard data unavailable."}
      </div>
    );
  }


  return (
    <div className="app-shell">

      <Sidebar />

      <main className="main-content">

        <Header />

        <div className="dashboard-content">

          <div className="stat-grid">

            <StatCard
              icon={<CreditCard size={21} />}
              title="Total Transactions"
              value={dashboardData.total_transactions.toLocaleString()}
              description="Dataset transactions"
              variant="purple"
            />

            <StatCard
              icon={<Activity size={21} />}
              title="Fraud Rate"
              value={`${(
                dashboardData.fraud_rate * 100
              ).toFixed(2)}%`}
              description={`${dashboardData.fraud_transactions.toLocaleString()} flagged as fraud`}
              variant="red"
            />

            <StatCard
              icon={<Network size={21} />}
              title="Network Risk Score"
              value={`${Math.round(
                dashboardData.network_risk_score * 100
              )} / 100`}
              description={
                dashboardData.network_risk_score >= 0.7
                  ? "High network risk"
                  : dashboardData.network_risk_score >= 0.4
                    ? "Medium network risk"
                    : "Low network risk"
              }
              variant="blue"
            />

            <StatCard
              icon={<BarChart3 size={21} />}
              title="Transaction Volume"
              value={`$${(
                dashboardData.total_amount / 1_000_000
              ).toFixed(2)}M`}
              description={`Average $${dashboardData.average_transaction_amount.toFixed(2)}`}
              variant="green"
            />

            <StatCard
              icon={<AlertTriangle size={21} />}
              title="Fraud Transactions"
              value={dashboardData.fraud_transactions.toLocaleString()}
              description={`${(
                dashboardData.fraud_rate * 100
              ).toFixed(2)}% of transactions`}
              variant="orange"
            />

          </div>


          <div className="dashboard-grid">

            <section className="card chart-card">

              <div className="card-header">
                <div>
                  <h2>Fraud Rate Trend</h2>

                  <p>
                    Recent fraud activity across the
                    monitoring window
                  </p>
                </div>

                <button className="secondary-button">
                  7 Days
                  <ChevronDown size={14} />
                </button>
              </div>

              <div className="chart-container">

                <ResponsiveContainer
                  width="100%"
                  height="100%"
                >

                  <AreaChart data={fraudTrend}>

                    <defs>
                      <linearGradient
                        id="fraudGradient"
                        x1="0"
                        y1="0"
                        x2="0"
                        y2="1"
                      >
                        <stop
                          offset="0%"
                          stopColor="#6F42C1"
                          stopOpacity={0.28}
                        />

                        <stop
                          offset="100%"
                          stopColor="#6F42C1"
                          stopOpacity={0.02}
                        />
                      </linearGradient>
                    </defs>

                    <CartesianGrid
                      strokeDasharray="3 3"
                      vertical={false}
                      stroke="#E5E7EB"
                    />

                    <XAxis
                      dataKey="day"
                      axisLine={false}
                      tickLine={false}
                      tick={{
                        fill: "#6B7280",
                        fontSize: 12,
                      }}
                    />

                    <YAxis
                      domain={[0, 5]}
                      tickFormatter={(value) =>
                        `${value}%`
                      }
                      axisLine={false}
                      tickLine={false}
                      tick={{
                        fill: "#6B7280",
                        fontSize: 12,
                      }}
                    />

                    <Tooltip
                      formatter={(value) => [
                        `${value}%`,
                        "Fraud rate",
                      ]}
                    />

                    <Area
                      type="monotone"
                      dataKey="rate"
                      stroke="#6F42C1"
                      strokeWidth={3}
                      fill="url(#fraudGradient)"
                    />

                  </AreaChart>

                </ResponsiveContainer>

              </div>

            </section>


            <NetworkIntelligence
              dashboardData={dashboardData}
            />


            <RecentTransactions
              transactions={recentTransactions}
              onSelectTransaction={
                handleSelectTransaction
              }
            />


            <RiskDistribution
              dashboardData={dashboardData}
            />

          </div>


          <section className="insights-card">

            <div className="insight-heading">

              <div className="insight-icon">
                <ShieldCheck size={21} />
              </div>

              <div>
                <h2>Risk Insights & Alerts</h2>

                <p>
                  Operational signals requiring attention
                </p>
              </div>

            </div>


            <div className="insight-items">

              <div className="insight-item">

                <span className="insight-marker red" />

                <div>
                  <strong>
                    Candidate abuse network detected
                  </strong>

                  <span>
                    Network intelligence identified
                    suspicious entity relationships.
                  </span>
                </div>

                <button>View</button>

              </div>


              <div className="insight-item">

                <span className="insight-marker orange" />

                <div>
                  <strong>
                    Multiple risk signals active
                  </strong>

                  <span>
                    Review transactions with elevated
                    behavioral risk.
                  </span>
                </div>

                <button>View</button>

              </div>


              <div className="insight-item">

                <span className="insight-marker purple" />

                <div>
                  <strong>
                    Network monitoring operational
                  </strong>

                  <span>
                    {dashboardData.fraud_spike
                      ? "A current fraud spike has been detected."
                      : "No current fraud spike detected."}
                  </span>
                </div>

                <button>View</button>

              </div>

            </div>

          </section>

        </div>

      </main>


      <InvestigationPanel
        transaction={selectedTransaction}
        loading={investigationLoading}
        error={investigationError}
        onClose={closeInvestigation}
      />

    </div>
  );
}


export default Dashboard;