import { useEffect, useRef, useState } from "react";
import {
  getDashboardSummary,
  getRecentTransactions,
  getTransactionInvestigation,
  scoreTransaction,
  getFraudTrend,
  getNetworkOverview,
  getSuspiciousDevices,
  getSuspiciousIPs,
} from "./services/api";

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
  Smartphone,
  Globe,
  Users,
  X,
  Clock3,
  AlertCircle,
  CheckCircle2,
  ArrowLeft,
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

// =========================================================
// Sidebar
// =========================================================

function Sidebar({ activeSection, onNavigate }) {
  const navigation = [
    {
      section: "OVERVIEW",
      items: [
        {
          id: "dashboard",
          label: "Dashboard",
          icon: LayoutDashboard,
        },
        {
          id: "transactions",
          label: "Transactions",
          icon: CreditCard,
        },
        {
          id: "investigation",
          label: "Investigation",
          icon: Search,
        },
      ],
    },
    {
      section: "INTELLIGENCE",
      items: [
        {
          id: "network",
          label: "Network Intelligence",
          icon: Network,
        },
        {
          id: "policies",
          label: "Rules & Policies",
          icon: Shield,
        },
        {
          id: "alerts",
          label: "Alerts",
          icon: Bell,
          badge: 5,
        },
        {
          id: "reports",
          label: "Reports",
          icon: BarChart3,
        },
      ],
    },
    {
      section: "SYSTEM",
      items: [
        {
          id: "settings",
          label: "Settings",
          icon: Settings,
        },
      ],
    },
  ];

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">
          <ShieldCheck size={25} />
        </div>

        <div>
          <div className="brand-name">RAZORSENTRY</div>

          <div className="brand-subtitle">
            Risk Intelligence
          </div>
        </div>
      </div>

      <nav className="nav">
        {navigation.map((group) => (
          <div key={group.section}>
            <div className="nav-section-title">
              {group.section}
            </div>

            {group.items.map((item) => {
              const Icon = item.icon;

              return (
                <button
                  key={item.id}
                  type="button"
                  className={`nav-item ${
                    activeSection === item.id ? "active" : ""
                  }`}
                  onClick={() => onNavigate(item.id)}
                >
                  <Icon size={19} />

                  <span>{item.label}</span>

                  {item.badge && (
                    <span className="nav-badge">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        ))}
      </nav>

      <div className="system-status">
        <div className="status-heading">
          SYSTEM STATUS
        </div>

        <div className="status-row">
          <span className="status-dot" />
          <span>All systems operational</span>
        </div>
      </div>
    </aside>
  );
}

// =========================================================
// Header
// =========================================================

function Header({
  onNavigate,
  dateRange,
  setDateRange,
  activeSection,
}) {
  const [dateMenuOpen, setDateMenuOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] =
    useState(false);

  const dateDropdownRef = useRef(null);
  const notificationRef = useRef(null);
  const profileRef = useRef(null);

  const dateOptions = [
    "Aug 28 – Sep 4, 2026",
    "Aug 21 – Sep 4, 2026",
    "Aug 6 – Sep 4, 2026",
  ];

  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (
        dateDropdownRef.current &&
        !dateDropdownRef.current.contains(event.target)
      ) {
        setDateMenuOpen(false);
      }

      if (
        notificationRef.current &&
        !notificationRef.current.contains(event.target)
      ) {
        setNotificationsOpen(false);
      }

      if (
        profileRef.current &&
        !profileRef.current.contains(event.target)
      ) {
        setProfileOpen(false);
      }
    };

    document.addEventListener(
      "mousedown",
      handleOutsideClick
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleOutsideClick
      );
    };
  }, []);

  const closeOtherMenus = (menu) => {
    if (menu !== "date") {
      setDateMenuOpen(false);
    }

    if (menu !== "notification") {
      setNotificationsOpen(false);
    }

    if (menu !== "profile") {
      setProfileOpen(false);
    }
  };

  const isNetworkView = activeSection === "network";

  return (
    <header className="header">
      <div>
        <h1>
          {isNetworkView ? "Network Intelligence" : "Dashboard"}
        </h1>

        <p>
          {isNetworkView
            ? "Connected entity and infrastructure risk analysis"
            : "Real-time payment risk intelligence overview"}
        </p>
      </div>

      <div className="header-actions">
        {/* DATE RANGE */}

        <div
          className="header-dropdown"
          ref={dateDropdownRef}
        >
          <button
            type="button"
            className={`date-button ${
              dateMenuOpen ? "open" : ""
            }`}
            onClick={() => {
              setDateMenuOpen(
                (previous) => !previous
              );
              closeOtherMenus("date");
            }}
          >
            <Activity size={16} />

            <span>{dateRange}</span>

            <ChevronDown
              size={15}
              className={
                dateMenuOpen ? "chevron-open" : ""
              }
            />
          </button>

          {dateMenuOpen && (
            <div className="dropdown-menu date-menu">
              <div className="dropdown-heading">
                Date range
              </div>

              {dateOptions.map((option) => (
                <button
                  type="button"
                  key={option}
                  className={
                    option === dateRange
                      ? "dropdown-selected"
                      : ""
                  }
                  onClick={() => {
                    setDateRange(option);
                    setDateMenuOpen(false);
                  }}
                >
                  <span>{option}</span>

                  {option === dateRange && (
                    <CheckCircle2 size={15} />
                  )}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* NOTIFICATIONS */}

        <div
          className="header-dropdown notification-wrapper"
          ref={notificationRef}
        >
          <button
            type="button"
            className={`icon-button notification ${
              notificationsOpen ? "open" : ""
            }`}
            onClick={() => {
              setNotificationsOpen(
                (previous) => !previous
              );
              closeOtherMenus("notification");
            }}
            aria-label="Open notifications"
            aria-expanded={notificationsOpen}
          >
            <Bell size={18} />

            <span>3</span>
          </button>

          {notificationsOpen && (
            <div className="notification-menu">
              <div className="notification-header">
                <div>
                  <strong>Notifications</strong>

                  <span>
                    Recent risk activity
                  </span>
                </div>

                <button
                  type="button"
                  className="notification-close"
                  onClick={() =>
                    setNotificationsOpen(false)
                  }
                  aria-label="Close notifications"
                >
                  <X size={16} />
                </button>
              </div>

              <div className="notification-item">
                <span className="notification-dot red" />

                <div>
                  <strong>
                    Candidate abuse network
                  </strong>

                  <span>
                    Suspicious entity relationships
                    were detected.
                  </span>
                </div>
              </div>

              <div className="notification-item">
                <span className="notification-dot orange" />

                <div>
                  <strong>
                    Elevated risk signals
                  </strong>

                  <span>
                    Some transactions require
                    investigator attention.
                  </span>
                </div>
              </div>

              <button
                type="button"
                className="notification-view-all"
                onClick={() => {
                  setNotificationsOpen(false);
                  onNavigate("alerts");
                }}
              >
                View all alerts
              </button>
            </div>
          )}
        </div>

        {/* PROFILE */}

        <div
          className="header-dropdown"
          ref={profileRef}
        >
          <button
            type="button"
            className={`profile ${
              profileOpen ? "open" : ""
            }`}
            onClick={() => {
              setProfileOpen(
                (previous) => !previous
              );
              closeOtherMenus("profile");
            }}
          >
            <div className="avatar">K</div>

            <div>
              <strong>Keerthana</strong>
              <small>Admin</small>
            </div>

            <ChevronDown
              size={15}
              className={
                profileOpen ? "chevron-open" : ""
              }
            />
          </button>

          {profileOpen && (
            <div className="dropdown-menu profile-menu">
              <button
                type="button"
                onClick={() => {
                  setProfileOpen(false);
                  onNavigate("settings");
                }}
              >
                <Settings size={15} />
                <span>Settings</span>
              </button>

              <button
                type="button"
                onClick={() => {
                  setProfileOpen(false);
                  onNavigate("reports");
                }}
              >
                <BarChart3 size={15} />
                <span>Reports</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

// =========================================================
// Stat Card
// =========================================================

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
        <span className="stat-title">
          {title}
        </span>

        <strong className="stat-value">
          {value}
        </strong>

        <span
          className={`stat-description ${variant}`}
        >
          {description}
        </span>
      </div>
    </div>
  );
}

// =========================================================
// Network Intelligence Summary
// =========================================================

function NetworkIntelligenceSummary({
  dashboardData,
  networkOverview,
  networkLoading,
  networkError,
  onNavigate,
}) {
  const [menuOpen, setMenuOpen] = useState(false);

  const networkRisk =
    dashboardData?.network_risk_score ?? 0;

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

          <p>
            Connected entities and shared
            infrastructure
          </p>
        </div>

        <div className="relative-action">
          <button
            type="button"
            className="more-button"
            onClick={() =>
              setMenuOpen(
                (previous) => !previous
              )
            }
            aria-label="Network options"
          >
            ...
          </button>

          {menuOpen && (
            <div className="small-menu">
              <button
                type="button"
                onClick={() => {
                  setMenuOpen(false);
                  onNavigate("network");
                }}
              >
                View network
              </button>

              <button
                type="button"
                onClick={() => {
                  setMenuOpen(false);
                  onNavigate("reports");
                }}
              >
                Open report
              </button>
            </div>
          )}
        </div>
      </div>

      {networkLoading ? (
        <div className="chart-loading">
          Loading network intelligence...
        </div>
      ) : networkError ? (
        <div className="chart-loading">
          {networkError}
        </div>
      ) : (
        <>
          <div className="network-list">
            <div className="network-item">
              <div className="network-icon purple">
                <Activity size={17} />
              </div>

              <div className="network-label">
                <strong>Network Risk</strong>

                <span>
                  {networkRiskLabel}
                </span>
              </div>

              <strong className="network-number">
                {Math.round(networkRisk * 100)}
                /100
              </strong>
            </div>

            <div className="network-item">
              <div className="network-icon orange">
                <Smartphone size={17} />
              </div>

              <div className="network-label">
                <strong>
                  Suspicious Devices
                </strong>

                <span>
                  Devices shared across customers
                </span>
              </div>

              <strong className="network-number">
                {(
                  networkOverview?.suspicious_devices ??
                  0
                ).toLocaleString()}
              </strong>
            </div>

            <div className="network-item">
              <div className="network-icon orange">
                <Globe size={17} />
              </div>

              <div className="network-label">
                <strong>
                  Suspicious IPs
                </strong>

                <span>
                  IPs shared across customers
                </span>
              </div>

              <strong className="network-number">
                {(
                  networkOverview?.suspicious_ips ??
                  0
                ).toLocaleString()}
              </strong>
            </div>

            <div className="network-item">
              <div className="network-icon red">
                <AlertTriangle size={17} />
              </div>

              <div className="network-label">
                <strong>
                  Connected Fraud
                </strong>

                <span>
                  Fraud linked to shared infrastructure
                </span>
              </div>

              <strong className="network-number">
                {(
                  networkOverview?.connected_fraud_transactions ??
                  0
                ).toLocaleString()}
              </strong>
            </div>
          </div>

          <div className="network-summary-note">
            <Network size={15} />

            <span className="network-description">
              Shared devices and IP addresses can reveal
              coordinated or connected fraudulent activity
              across customers.
            </span>
          </div>

          <button
            type="button"
            className="primary-button"
            onClick={() =>
              onNavigate("network")
            }
          >
            <Network size={16} />
            View Network Intelligence
          </button>
        </>
      )}
    </section>
  );
}

// =========================================================
// Network Intelligence Workspace
// =========================================================

function NetworkIntelligencePage({
  networkOverview,
  suspiciousDevices,
  suspiciousIPs,
  networkLoading,
  networkError,
  dashboardData,
  onBack,
}) {
  const networkRisk =
    dashboardData?.network_risk_score ?? 0;

  const networkRiskLabel =
    networkRisk >= 0.7
      ? "High"
      : networkRisk >= 0.4
        ? "Medium"
        : "Low";

  if (networkLoading) {
    return (
      <div className="dashboard-content">
        <div className="card">
          <div className="chart-loading">
            Loading network intelligence...
          </div>
        </div>
      </div>
    );
  }

  if (networkError) {
    return (
      <div className="dashboard-content">
        <div className="card network-error-card">
          <div className="chart-loading">
            {networkError}
          </div>

          <button
            type="button"
            className="secondary-button"
            onClick={onBack}
          >
            <ArrowLeft size={15} />
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-content">
      {/* PAGE HEADER */}

      <div className="network-workspace-header">
        <div>
          <button
            type="button"
            className="secondary-button"
            onClick={onBack}
          >
            <ArrowLeft size={15} />
            Back to Dashboard
          </button>
        </div>

        <div className="network-workspace-intro">
          <div className="section-header-icon blue">
            <Network size={20} />
          </div>

          <div>
            <h2>Network Intelligence</h2>

            <p>
              Investigate connected customers,
              devices, IP addresses and fraud
              relationships.
            </p>
          </div>
        </div>
      </div>

      {/* NETWORK OVERVIEW */}

      <div className="stat-grid">
        <StatCard
          icon={<Users size={21} />}
          title="Customers"
          value={(
            networkOverview?.customers ?? 0
          ).toLocaleString()}
          description="Customers observed"
          variant="purple"
        />

        <StatCard
          icon={<Smartphone size={21} />}
          title="Devices"
          value={(
            networkOverview?.devices ?? 0
          ).toLocaleString()}
          description="Unique devices"
          variant="blue"
        />

        <StatCard
          icon={<Globe size={21} />}
          title="IP Addresses"
          value={(
            networkOverview?.ips ?? 0
          ).toLocaleString()}
          description="Unique IP addresses"
          variant="blue"
        />

        <StatCard
          icon={<AlertTriangle size={21} />}
          title="Connected Fraud"
          value={(
            networkOverview?.connected_fraud_transactions ??
            0
          ).toLocaleString()}
          description="Fraud linked to infrastructure"
          variant="red"
        />
      </div>

      {/* NETWORK RISK */}

      <section className="card">
        <div className="card-header">
          <div>
            <h2>Network Risk Overview</h2>

            <p>
              Aggregated risk from connected
              infrastructure
            </p>
          </div>

          <div className="section-header-icon purple">
            <Activity size={18} />
          </div>
        </div>

        <div className="network-list">
          <div className="network-item">
            <div className="network-icon purple">
              <Activity size={17} />
            </div>

            <div className="network-label">
              <strong>
                Overall Network Risk
              </strong>

              <span>
                Current aggregated network risk
                score
              </span>
            </div>

            <strong className="network-number">
              {Math.round(networkRisk * 100)}
              /100
            </strong>
          </div>

          <div className="network-item">
            <div className="network-icon orange">
              <Smartphone size={17} />
            </div>

            <div className="network-label">
              <strong>
                Suspicious Devices
              </strong>

              <span>
                Shared across multiple customers
              </span>
            </div>

            <strong className="network-number">
              {(
                networkOverview?.suspicious_devices ??
                0
              ).toLocaleString()}
            </strong>
          </div>

          <div className="network-item">
            <div className="network-icon orange">
              <Globe size={17} />
            </div>

            <div className="network-label">
              <strong>
                Suspicious IP Addresses
              </strong>

              <span>
                Shared across multiple customers
              </span>
            </div>

            <strong className="network-number">
              {(
                networkOverview?.suspicious_ips ??
                0
              ).toLocaleString()}
            </strong>
          </div>

          <div className="network-item">
            <div className="network-icon red">
              <AlertTriangle size={17} />
            </div>

            <div className="network-label">
              <strong>
                Connected Fraud Transactions
              </strong>

              <span>
                Fraud associated with shared
                infrastructure
              </span>
            </div>

            <strong className="network-number">
              {(
                networkOverview?.connected_fraud_transactions ??
                0
              ).toLocaleString()}
            </strong>
          </div>
        </div>

        <div className="network-summary-note">
          <ShieldCheck size={16} />

          <span>
            Network risk currently evaluates as{" "}
            <strong>
              {networkRiskLabel} risk
            </strong>
            . Shared infrastructure provides
            additional context beyond individual
            transaction-level signals.
          </span>
        </div>
      </section>

      {/* SUSPICIOUS DEVICES */}

      <section className="card">
        <div className="card-header">
          <div>
            <h2>Suspicious Devices</h2>

            <p>
              Devices associated with multiple
              customers and elevated fraud activity
            </p>
          </div>

          <div className="section-header-icon orange">
            <Smartphone size={18} />
          </div>
        </div>

        <div className="transaction-table-wrapper">
          <table>
            <thead>
              <tr>
                <th>DEVICE</th>
                <th>CUSTOMERS</th>
                <th>TRANSACTIONS</th>
                <th>FRAUD</th>
                <th>FRAUD RATE</th>
                <th>MAX RISK</th>
              </tr>
            </thead>

            <tbody>
              {suspiciousDevices.length === 0 ? (
                <tr>
                  <td
                    colSpan="6"
                    className="time"
                  >
                    No suspicious devices detected.
                  </td>
                </tr>
              ) : (
                suspiciousDevices.map(
                  (device) => (
                    <tr
                      key={device.device_id}
                      className="transaction-row"
                    >
                      <td>
                        <div className="transaction-id">
                          <span className="risk-dot red" />

                          {device.device_id}
                        </div>
                      </td>

                      <td>{device.customers}</td>

                      <td>{device.transactions}</td>

                      <td>
                        <span className="score red">
                          {device.fraudulent}
                        </span>
                      </td>

                      <td>
                        {Number(
                          device.fraud_rate
                        ).toFixed(2)}
                        %
                      </td>

                      <td>
                        <span className="score red">
                          {Number(
                            device.max_risk_score
                          ).toFixed(2)}
                        </span>
                      </td>
                    </tr>
                  )
                )
              )}
            </tbody>
          </table>
        </div>
      </section>

      {/* SUSPICIOUS IPS */}

      <section className="card">
        <div className="card-header">
          <div>
            <h2>Suspicious IP Addresses</h2>

            <p>
              IP addresses shared across customers
              with elevated fraud activity
            </p>
          </div>

          <div className="section-header-icon orange">
            <Globe size={18} />
          </div>
        </div>

        <div className="transaction-table-wrapper">
          <table>
            <thead>
              <tr>
                <th>IP ADDRESS</th>
                <th>CUSTOMERS</th>
                <th>TRANSACTIONS</th>
                <th>FRAUD</th>
                <th>FRAUD RATE</th>
                <th>MAX RISK</th>
              </tr>
            </thead>

            <tbody>
              {suspiciousIPs.length === 0 ? (
                <tr>
                  <td
                    colSpan="6"
                    className="time"
                  >
                    No suspicious IP addresses
                    detected.
                  </td>
                </tr>
              ) : (
                suspiciousIPs.map(
                  (ip) => (
                    <tr
                      key={ip.ip_address}
                      className="transaction-row"
                    >
                      <td>
                        <div className="transaction-id">
                          <span className="risk-dot red" />

                          {ip.ip_address}
                        </div>
                      </td>

                      <td>{ip.customers}</td>

                      <td>{ip.transactions}</td>

                      <td>
                        <span className="score red">
                          {ip.fraudulent}
                        </span>
                      </td>

                      <td>
                        {Number(
                          ip.fraud_rate
                        ).toFixed(2)}
                        %
                      </td>

                      <td>
                        <span className="score red">
                          {Number(
                            ip.max_risk_score
                          ).toFixed(2)}
                        </span>
                      </td>
                    </tr>
                  )
                )
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

// =========================================================
// Risk Distribution
// =========================================================

function RiskDistribution({
  dashboardData,
}) {
  const total =
    dashboardData.total_transactions;

  const fraud =
    dashboardData.fraud_transactions;

  const legitimate =
    dashboardData.legitimate_transactions;

  const fraudPercentage = total
    ? ((fraud / total) * 100).toFixed(1)
    : "0.0";

  const legitimatePercentage = total
    ? ((legitimate / total) * 100).toFixed(1)
    : "0.0";

  return (
    <section
      className="card distribution-card"
      id="distribution-section"
    >
      <div className="card-header">
        <div>
          <h2>Transaction Outcome</h2>

          <p>
            Ground-truth dataset distribution
          </p>
        </div>
      </div>

      <div className="distribution">
        <div className="donut">
          <div className="donut-center">
            <strong>
              {total.toLocaleString()}
            </strong>

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

// =========================================================
// Investigation Panel
// =========================================================

function InvestigationPanel({
  transaction,
  loading,
  error,
  onClose,
  mlScore,
  mlLoading,
  mlError,
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
              {transaction?.transaction_id ||
                "Loading..."}
            </h2>
          </div>

          <button
            type="button"
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
              <strong>
                Investigation unavailable
              </strong>

              <span>{error}</span>
            </div>
          </div>
        )}

        {transaction &&
          !loading &&
          !error && (
            <div className="investigation-content">
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

              {/* Live ML Decision */}

              <div className="investigation-section">
                <div className="investigation-section-title">
                  <ShieldCheck size={16} />
                  Live ML Decision
                </div>

                {mlLoading && (
                  <div className="investigation-loading">
                    <div className="investigation-spinner" />
                    Running fraud model...
                  </div>
                )}

                {mlError &&
                  !mlLoading && (
                    <div className="investigation-error">
                      <AlertCircle size={20} />

                      <div>
                        <strong>
                          ML scoring unavailable
                        </strong>

                        <span>
                          {mlError}
                        </span>
                      </div>
                    </div>
                  )}

                {mlScore &&
                  !mlLoading &&
                  !mlError && (
                    <>
                      <div className="ml-decision-card">
                        <div className="ml-metric">
                          <span>
                            ML FRAUD PROBABILITY
                          </span>

                          <strong>
                            {(
                              mlScore.fraud_probability *
                              100
                            ).toFixed(1)}
                            %
                          </strong>
                        </div>

                        <div className="ml-metric">
                          <span>
                            COMBINED RISK SCORE
                          </span>

                          <strong>
                            {Number(
                              mlScore.risk_score
                            ).toFixed(3)}
                          </strong>
                        </div>

                        <div className="ml-decision">
                          <span>
                            POLICY DECISION
                          </span>

                          <strong
                            className={`policy-decision ${mlScore.decision.toLowerCase()}`}
                          >
                            {mlScore.decision}
                          </strong>
                        </div>
                      </div>

                      {/* ML Explainability */}

                      {Array.isArray(
                        mlScore.reasons
                      ) &&
                        mlScore.reasons.length >
                          0 && (
                          <div className="ml-risk-reasons">
                            <div className="ml-risk-reasons-header">
                              <AlertTriangle size={15} />

                              <span>
                                WHY THIS DECISION
                              </span>
                            </div>

                            <div className="ml-risk-reasons-list">
                              {mlScore.reasons.map(
                                (
                                  reason,
                                  index
                                ) => (
                                  <div
                                    className="ml-risk-reason"
                                    key={`${reason}-${index}`}
                                  >
                                    <span className="risk-reason-dot" />

                                    <span>
                                      {reason}
                                    </span>
                                  </div>
                                )
                              )}
                            </div>
                          </div>
                        )}
                    </>
                  )}
              </div>

              {/* Transaction Details */}

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
                      {Number(
                        transaction.amount
                      ).toFixed(2)}
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

              {/* Risk Signals */}

              <div className="investigation-section">
                <div className="investigation-section-title">
                  <AlertTriangle size={16} />
                  Risk Signals
                </div>

                {transaction.risk_reasons?.length >
                0 ? (
                  <div className="risk-reason-list">
                    {transaction.risk_reasons.map(
                      (reason, index) => (
                        <div
                          className="risk-reason"
                          key={`${reason}-${index}`}
                        >
                          <span className="risk-reason-dot" />

                          <span>
                            {reason}
                          </span>
                        </div>
                      )
                    )}
                  </div>
                ) : (
                  <div className="no-risk-signals">
                    No rule-based risk signals
                    detected.
                  </div>
                )}
              </div>

              {/* Behavioral Signals */}

              <div className="investigation-section">
                <div className="investigation-section-title">
                  <Activity size={16} />
                  Behavioral Signals
                </div>

                <div className="signal-grid">
                  <div className="signal-card">
                    <Clock3 size={15} />

                    <span>
                      Customer velocity · 5m
                    </span>

                    <strong>
                      {
                        transaction.customer_velocity_5m
                      }
                    </strong>
                  </div>

                  <div className="signal-card">
                    <Clock3 size={15} />

                    <span>
                      Customer velocity · 1h
                    </span>

                    <strong>
                      {
                        transaction.customer_velocity_1h
                      }
                    </strong>
                  </div>

                  <div className="signal-card">
                    <Smartphone size={15} />

                    <span>
                      Device velocity · 5m
                    </span>

                    <strong>
                      {transaction.device_velocity_5m}
                    </strong>
                  </div>

                  <div className="signal-card">
                    <Globe size={15} />

                    <span>
                      IP velocity · 5m
                    </span>

                    <strong>
                      {transaction.ip_velocity_5m}
                    </strong>
                  </div>

                  <div className="signal-card">
                    <AlertTriangle size={15} />

                    <span>
                      Failed attempts · 1h
                    </span>

                    <strong>
                      {transaction.failed_attempts_1h}
                    </strong>
                  </div>

                  <div className="signal-card">
                    <Users size={15} />

                    <span>
                      Shared device
                    </span>

                    <strong>
                      {transaction.shared_device_flag
                        ? "Yes"
                        : "No"}
                    </strong>
                  </div>

                  <div className="signal-card">
                    <Network size={15} />

                    <span>
                      Shared IP
                    </span>

                    <strong>
                      {transaction.shared_ip_flag
                        ? "Yes"
                        : "No"}
                    </strong>
                  </div>
                </div>
              </div>

              <div className="investigation-note">
                <ShieldCheck size={17} />

                <div>
                  <strong>
                    Investigator view
                  </strong>

                  <span>
                    RazorSentry combines behavioral
                    signals, calibrated ML scoring,
                    and policy logic to produce an
                    actionable transaction decision.
                  </span>
                </div>
              </div>
            </div>
          )}
      </div>
    </div>
  );
}

// =========================================================
// Recent Transactions
// =========================================================

function RecentTransactions({
  transactions,
  onSelectTransaction,
  showAll,
  setShowAll,
}) {
  const visibleTransactions = showAll
    ? transactions
    : transactions.slice(0, 8);

  return (
    <section
      className="card transactions-card"
      id="transactions-section"
    >
      <div className="card-header">
        <div>
          <h2>Recent Transactions</h2>

          <p>
            Latest transactions evaluated by
            RazorSentry
          </p>
        </div>

        <button
          type="button"
          className="secondary-button"
          onClick={() =>
            setShowAll(
              (previous) => !previous
            )
          }
        >
          {showAll ? "Show Less" : "View All"}
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
            {visibleTransactions.length === 0 ? (
              <tr>
                <td
                  colSpan="6"
                  className="time"
                >
                  No recent transactions available.
                </td>
              </tr>
            ) : (
              visibleTransactions.map(
                (transaction) => {
                  const risk =
                    transaction.risk_level ||
                    "low";

                  const score =
                    transaction.risk_score ?? 0;

                  return (
                    <tr
                      key={
                        transaction.transaction_id
                      }
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

                          {
                            transaction.transaction_id
                          }
                        </div>
                      </td>

                      <td className="amount">
                        {transaction.currency}{" "}
                        {Number(
                          transaction.amount
                        ).toFixed(2)}
                      </td>

                      <td className="customer">
                        {transaction.customer_id ||
                          "—"}
                      </td>

                      <td>
                        <span
                          className={`score ${risk}`}
                        >
                          {Number(
                            score
                          ).toFixed(2)}
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
                }
              )
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

// =========================================================
// Rules & Policies
// =========================================================

function PoliciesSection() {
  return (
    <section
      className="card intelligence-section-card"
      id="policies-section"
    >
      <div className="card-header">
        <div>
          <h2>Rules & Policies</h2>

          <p>
            How RazorSentry converts risk signals
            into actionable decisions
          </p>
        </div>

        <div className="section-header-icon purple">
          <Shield size={18} />
        </div>
      </div>

      <div className="network-list">
        <div className="network-item">
          <div className="network-icon purple">
            <AlertTriangle size={17} />
          </div>

          <div className="network-label">
            <strong>Rule-based signals</strong>

            <span>
              Deterministic behavioral and
              transaction rules contribute to
              overall risk.
            </span>
          </div>

          <span className="network-status safe">
            Active
          </span>
        </div>

        <div className="network-item">
          <div className="network-icon blue">
            <ShieldCheck size={17} />
          </div>

          <div className="network-label">
            <strong>Calibrated ML scoring</strong>

            <span>
              Model probability is combined with
              rule-based risk.
            </span>
          </div>

          <span className="network-status safe">
            Active
          </span>
        </div>

        <div className="network-item">
          <div className="network-icon red">
            <AlertTriangle size={17} />
          </div>

          <div className="network-label">
            <strong>HOLD</strong>

            <span>
              High-risk transactions can be
              stopped for investigation.
            </span>
          </div>

          <span className="network-status warning">
            High Risk
          </span>
        </div>

        <div className="network-item">
          <div className="network-icon orange">
            <Search size={17} />
          </div>

          <div className="network-label">
            <strong>REVIEW</strong>

            <span>
              Elevated-risk transactions can be
              routed to an investigator.
            </span>
          </div>

          <span className="network-status warning">
            Review
          </span>
        </div>

        <div className="network-item">
          <div className="network-icon green">
            <CheckCircle2 size={17} />
          </div>

          <div className="network-label">
            <strong>ALLOW</strong>

            <span>
              Low-risk transactions can continue
              automatically.
            </span>
          </div>

          <span className="network-status safe">
            Auto
          </span>
        </div>
      </div>
    </section>
  );
}

// =========================================================
// Alerts
// =========================================================

function AlertsSection({
  dashboardData,
  onNavigate,
}) {
  return (
    <section
      className="card intelligence-section-card"
      id="alerts-section"
    >
      <div className="card-header">
        <div>
          <h2>Risk Alerts</h2>

          <p>
            Operational signals currently
            requiring attention
          </p>
        </div>

        <div className="section-header-icon orange">
          <Bell size={18} />
        </div>
      </div>

      <div className="network-list">
        <div className="network-item">
          <div className="network-icon red">
            <GitBranch size={17} />
          </div>

          <div className="network-label">
            <strong>
              Candidate abuse network
            </strong>

            <span>
              Network intelligence identified
              suspicious entity relationships.
            </span>
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
              : "Clear"}
          </span>
        </div>

        <div className="network-item">
          <div className="network-icon orange">
            <Activity size={17} />
          </div>

          <div className="network-label">
            <strong>
              Fraud monitoring
            </strong>

            <span>
              Current fraud activity across
              the monitoring window.
            </span>
          </div>

          <span
            className={`network-status ${
              dashboardData.fraud_spike
                ? "warning"
                : "safe"
            }`}
          >
            {dashboardData.fraud_spike
              ? "Spike"
              : "Normal"}
          </span>
        </div>

        <div className="network-item">
          <div className="network-icon purple">
            <Search size={17} />
          </div>

          <div className="network-label">
            <strong>
              Behavioral review
            </strong>

            <span>
              Investigate transactions with
              elevated behavioral signals.
            </span>
          </div>

          <button
            type="button"
            className="inline-action"
            onClick={() =>
              onNavigate("transactions")
            }
          >
            Review
          </button>
        </div>
      </div>
    </section>
  );
}

// =========================================================
// Reports
// =========================================================

function ReportsSection({
  dashboardData,
}) {
  return (
    <section
      className="card intelligence-section-card"
      id="reports-section"
    >
      <div className="card-header">
        <div>
          <h2>Risk Reports</h2>

          <p>
            Current monitoring and risk summary
          </p>
        </div>

        <div className="section-header-icon blue">
          <BarChart3 size={18} />
        </div>
      </div>

      <div className="network-list">
        <div className="network-item">
          <div className="network-icon purple">
            <CreditCard size={17} />
          </div>

          <div className="network-label">
            <strong>
              Transactions monitored
            </strong>

            <span>
              Total transactions evaluated
              by RazorSentry.
            </span>
          </div>

          <strong className="network-number">
            {dashboardData.total_transactions.toLocaleString()}
          </strong>
        </div>

        <div className="network-item">
          <div className="network-icon red">
            <AlertTriangle size={17} />
          </div>

          <div className="network-label">
            <strong>
              Fraud transactions
            </strong>

            <span>
              Ground-truth fraudulent
              transactions in the dataset.
            </span>
          </div>

          <strong className="network-number">
            {dashboardData.fraud_transactions.toLocaleString()}
          </strong>
        </div>

        <div className="network-item">
          <div className="network-icon orange">
            <Activity size={17} />
          </div>

          <div className="network-label">
            <strong>
              Fraud rate
            </strong>

            <span>
              Share of transactions labeled
              as fraudulent.
            </span>
          </div>

          <strong className="network-number">
            {(dashboardData.fraud_rate * 100).toFixed(2)}%
          </strong>
        </div>

        <div className="network-item">
          <div className="network-icon blue">
            <Network size={17} />
          </div>

          <div className="network-label">
            <strong>
              Network risk
            </strong>

            <span>
              Aggregated network-level
              intelligence score.
            </span>
          </div>

          <strong className="network-number">
            {Math.round(
              dashboardData.network_risk_score * 100
            )}
            /100
          </strong>
        </div>
      </div>
    </section>
  );
}

// =========================================================
// Settings
// =========================================================

function SettingsSection() {
  return (
    <section
      className="card intelligence-section-card"
      id="settings-section"
    >
      <div className="card-header">
        <div>
          <h2>System Status</h2>

          <p>
            Current RazorSentry service
            configuration
          </p>
        </div>

        <div className="section-header-icon blue">
          <Settings size={18} />
        </div>
      </div>

      <div className="network-list">
        <div className="network-item">
          <div className="network-icon green">
            <CheckCircle2 size={17} />
          </div>

          <div className="network-label">
            <strong>Dashboard data</strong>

            <span>
              Live dashboard data connection
            </span>
          </div>

          <span className="network-status safe">
            Connected
          </span>
        </div>

        <div className="network-item">
          <div className="network-icon green">
            <ShieldCheck size={17} />
          </div>

          <div className="network-label">
            <strong>ML scoring API</strong>

            <span>
              Calibrated fraud scoring service
            </span>
          </div>

          <span className="network-status safe">
            Enabled
          </span>
        </div>

        <div className="network-item">
          <div className="network-icon blue">
            <Network size={17} />
          </div>

          <div className="network-label">
            <strong>Network intelligence</strong>

            <span>
              Aggregated entity-level monitoring
            </span>
          </div>

          <span className="network-status safe">
            Enabled
          </span>
        </div>

        <div className="network-item">
          <div className="network-icon purple">
            <Search size={17} />
          </div>

          <div className="network-label">
            <strong>
              Transaction investigation
            </strong>

            <span>
              Behavioral and transaction detail
              lookup
            </span>
          </div>

          <span className="network-status safe">
            Enabled
          </span>
        </div>

        <div className="network-item">
          <div className="network-icon orange">
            <Shield size={17} />
          </div>

          <div className="network-label">
            <strong>Policy engine</strong>

            <span>
              ALLOW, REVIEW and HOLD decisions
            </span>
          </div>

          <span className="network-status safe">
            Enabled
          </span>
        </div>
      </div>
    </section>
  );
}

// =========================================================
// Risk Insights
// =========================================================

function RiskInsights({
  dashboardData,
  onNavigate,
}) {
  return (
    <section
      className="insights-card"
      id="insights-section"
    >
      <div className="insight-heading">
        <div className="insight-icon">
          <ShieldCheck size={21} />
        </div>

        <div>
          <h2>Risk Insights & Alerts</h2>

          <p>
            Operational signals requiring
            attention
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

          <button
            type="button"
            onClick={() =>
              onNavigate("network")
            }
          >
            View
          </button>
        </div>

        <div className="insight-item">
          <span className="insight-marker orange" />

          <div>
            <strong>
              Multiple risk signals active
            </strong>

            <span>
              Review transactions with
              elevated behavioral risk.
            </span>
          </div>

          <button
            type="button"
            onClick={() =>
              onNavigate("transactions")
            }
          >
            View
          </button>
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

          <button
            type="button"
            onClick={() =>
              onNavigate("alerts")
            }
          >
            View
          </button>
        </div>
      </div>
    </section>
  );
}

// =========================================================
// Dashboard
// =========================================================

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

  const [mlScore, setMlScore] =
    useState(null);

  const [mlLoading, setMlLoading] =
    useState(false);

  const [mlError, setMlError] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [activeSection, setActiveSection] =
    useState("dashboard");

  const [dateRange, setDateRange] =
    useState("Aug 28 – Sep 4, 2026");

  // =======================================================
  // Fraud trend state
  // =======================================================

  const [trendRange, setTrendRange] =
    useState("7 Days");

  const [trendMenuOpen, setTrendMenuOpen] =
    useState(false);

  const [trendData, setTrendData] =
    useState([]);

  const [trendLoading, setTrendLoading] =
    useState(false);

  const [trendError, setTrendError] =
    useState("");

  const [showAllTransactions, setShowAllTransactions] =
    useState(false);

  // =======================================================
  // Network intelligence state
  // =======================================================

  const [networkOverview, setNetworkOverview] =
    useState(null);

  const [suspiciousDevices, setSuspiciousDevices] =
    useState([]);

  const [suspiciousIPs, setSuspiciousIPs] =
    useState([]);

  const [networkLoading, setNetworkLoading] =
    useState(false);

  const [networkError, setNetworkError] =
    useState("");

  // =======================================================
  // Refs
  // =======================================================

  const dashboardRef = useRef(null);
  const transactionsRef = useRef(null);
  const policiesRef = useRef(null);
  const alertsRef = useRef(null);
  const reportsRef = useRef(null);
  const settingsRef = useRef(null);

  const trendDropdownRef = useRef(null);

  // =======================================================
  // Load fraud trend
  // =======================================================

  useEffect(() => {
    const loadFraudTrend = async () => {
      setTrendLoading(true);
      setTrendError("");

      try {
        const days =
          trendRange === "7 Days"
            ? 7
            : trendRange === "14 Days"
              ? 14
              : 30;

        const response =
          await getFraudTrend(days);

        const formattedData =
          response.data.map((item) => ({
            day: new Date(
              `${item.date}T00:00:00`
            ).toLocaleDateString(
              "en-US",
              {
                month: "short",
                day: "numeric",
              }
            ),
            rate: item.fraud_rate,
          }));

        setTrendData(formattedData);
      } catch (error) {
        console.error(
          "Failed to load fraud trend:",
          error
        );

        setTrendError(
          "Unable to load fraud trend."
        );

        setTrendData([]);
      } finally {
        setTrendLoading(false);
      }
    };

    loadFraudTrend();
  }, [trendRange]);

  // =======================================================
  // Load network intelligence
  // =======================================================

  useEffect(() => {
    const loadNetworkIntelligence = async () => {
      setNetworkLoading(true);
      setNetworkError("");

      try {
        const [
          overview,
          devices,
          ips,
        ] = await Promise.all([
          getNetworkOverview(),
          getSuspiciousDevices(10),
          getSuspiciousIPs(10),
        ]);

        setNetworkOverview(overview);

        setSuspiciousDevices(
          devices.data || []
        );

        setSuspiciousIPs(
          ips.data || []
        );
      } catch (error) {
        console.error(
          "Failed to load network intelligence:",
          error
        );

        setNetworkError(
          "Unable to load network intelligence."
        );

        setNetworkOverview(null);
        setSuspiciousDevices([]);
        setSuspiciousIPs([]);
      } finally {
        setNetworkLoading(false);
      }
    };

    loadNetworkIntelligence();
  }, []);

  // =======================================================
  // Close trend dropdown on outside click
  // =======================================================

  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (
        trendDropdownRef.current &&
        !trendDropdownRef.current.contains(
          event.target
        )
      ) {
        setTrendMenuOpen(false);
      }
    };

    document.addEventListener(
      "mousedown",
      handleOutsideClick
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleOutsideClick
      );
    };
  }, []);

  // =======================================================
  // Navigation
  // =======================================================

  const sectionRefs = {
    dashboard: dashboardRef,
    transactions: transactionsRef,
    policies: policiesRef,
    alerts: alertsRef,
    reports: reportsRef,
    settings: settingsRef,
  };

  const scrollToSection = (section) => {
    // Network is now a dedicated workspace.

    if (section === "network") {
      setActiveSection("network");

      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });

      return;
    }

    // Investigation is opened by selecting a transaction.

    if (section === "investigation") {
      return;
    }

    setActiveSection(section);

    const targetRef =
      sectionRefs[section];

    if (!targetRef?.current) {
      return;
    }

    targetRef.current.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  // =======================================================
  // Update active navigation
  // =======================================================

  useEffect(() => {
    if (activeSection === "network") {
      return;
    }

    const sections = [
      ["dashboard", dashboardRef],
      ["transactions", transactionsRef],
      ["policies", policiesRef],
      ["alerts", alertsRef],
      ["reports", reportsRef],
      ["settings", settingsRef],
    ];

    const observer =
      new IntersectionObserver(
        (entries) => {
          const visible = entries
            .filter(
              (entry) =>
                entry.isIntersecting
            )
            .sort(
              (a, b) =>
                b.intersectionRatio -
                a.intersectionRatio
            );

          if (visible.length === 0) {
            return;
          }

          const currentId =
            visible[0].target.id;

          const matched =
            sections.find(
              ([, ref]) =>
                ref.current?.id ===
                currentId
            );

          if (matched) {
            setActiveSection(
              matched[0]
            );
          }
        },
        {
          root: null,
          rootMargin:
            "-18% 0px -65% 0px",
          threshold: [
            0.1,
            0.25,
            0.5,
          ],
        }
      );

    sections.forEach(([, ref]) => {
      if (ref.current) {
        observer.observe(ref.current);
      }
    });

    return () => {
      observer.disconnect();
    };
  }, [activeSection]);

  // =======================================================
  // Load dashboard
  // =======================================================

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

        setDashboardData(
          dashboardSummary
        );

        setRecentTransactions(
          transactions.map(
            (transaction) => ({
              ...transaction,
              customer_id:
                transaction.customer_id ||
                null,
            })
          )
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

  // =======================================================
  // Transaction investigation + ML
  // =======================================================

  const handleSelectTransaction = async (
    transactionId
  ) => {
    setActiveSection("investigation");

    setSelectedTransaction(null);
    setInvestigationError("");
    setInvestigationLoading(true);

    setMlScore(null);
    setMlError("");
    setMlLoading(true);

    try {
      const [
        investigation,
        score,
      ] = await Promise.all([
        getTransactionInvestigation(
          transactionId
        ),
        scoreTransaction(
          transactionId
        ),
      ]);

      setSelectedTransaction(
        investigation
      );

      setMlScore(score);
    } catch (err) {
      console.error(
        "Failed to load transaction intelligence:",
        err
      );

      const message =
        err.response?.data?.detail ||
        "Unable to load transaction intelligence.";

      setInvestigationError(message);
      setMlError(message);
    } finally {
      setInvestigationLoading(false);
      setMlLoading(false);
    }
  };

  // =======================================================
  // Close investigation
  // =======================================================

  const closeInvestigation = () => {
    setSelectedTransaction(null);
    setInvestigationError("");
    setInvestigationLoading(false);

    setMlScore(null);
    setMlError("");
    setMlLoading(false);

    setActiveSection("transactions");
  };

  // =======================================================
  // Loading
  // =======================================================

  if (loading) {
    return (
      <div className="loading-screen">
        Loading RazorSentry...
      </div>
    );
  }

  // =======================================================
  // Error
  // =======================================================

  if (error || !dashboardData) {
    return (
      <div className="loading-screen">
        {error ||
          "Dashboard data unavailable."}
      </div>
    );
  }

  // =======================================================
  // UI
  // =======================================================

  const showingNetworkWorkspace =
    activeSection === "network";

  return (
    <div className="app-shell">
      <Sidebar
        activeSection={activeSection}
        onNavigate={scrollToSection}
      />

      <main className="main-content">
        <Header
          onNavigate={scrollToSection}
          dateRange={dateRange}
          setDateRange={setDateRange}
          activeSection={activeSection}
        />

        {showingNetworkWorkspace ? (
          <NetworkIntelligencePage
            networkOverview={
              networkOverview
            }
            suspiciousDevices={
              suspiciousDevices
            }
            suspiciousIPs={
              suspiciousIPs
            }
            networkLoading={
              networkLoading
            }
            networkError={
              networkError
            }
            dashboardData={
              dashboardData
            }
            onBack={() =>
              scrollToSection("dashboard")
            }
          />
        ) : (
          <div
            className="dashboard-content"
            ref={dashboardRef}
            id="dashboard-section"
          >
            {/* =================================================
                STATS
            ================================================= */}

            <div className="stat-grid">
              <StatCard
                icon={
                  <CreditCard size={21} />
                }
                title="Total Transactions"
                value={dashboardData.total_transactions.toLocaleString()}
                description="Dataset transactions"
                variant="purple"
              />

              <StatCard
                icon={
                  <Activity size={21} />
                }
                title="Fraud Rate"
                value={`${(
                  dashboardData.fraud_rate *
                  100
                ).toFixed(2)}%`}
                description={`${dashboardData.fraud_transactions.toLocaleString()} flagged as fraud`}
                variant="red"
              />

              <StatCard
                icon={
                  <Network size={21} />
                }
                title="Network Risk Score"
                value={`${Math.round(
                  dashboardData.network_risk_score *
                    100
                )} / 100`}
                description={
                  dashboardData.network_risk_score >=
                  0.7
                    ? "High network risk"
                    : dashboardData.network_risk_score >=
                        0.4
                      ? "Medium network risk"
                      : "Low network risk"
                }
                variant="blue"
              />

              <StatCard
                icon={
                  <BarChart3 size={21} />
                }
                title="Transaction Volume"
                value={`$${(
                  dashboardData.total_amount /
                  1_000_000
                ).toFixed(2)}M`}
                description={`Average $${dashboardData.average_transaction_amount.toFixed(
                  2
                )}`}
                variant="green"
              />

              <StatCard
                icon={
                  <AlertTriangle size={21} />
                }
                title="Fraud Transactions"
                value={dashboardData.fraud_transactions.toLocaleString()}
                description={`${(
                  dashboardData.fraud_rate *
                  100
                ).toFixed(2)}% of transactions`}
                variant="orange"
              />
            </div>

            {/* =================================================
                MAIN DASHBOARD GRID
            ================================================= */}

            <div className="dashboard-grid">
              {/* Fraud Trend */}

              <section className="card chart-card">
                <div className="card-header">
                  <div>
                    <h2>Fraud Rate Trend</h2>

                    <p>
                      Recent fraud activity across
                      the monitoring window
                    </p>
                  </div>

                  <div
                    className="header-dropdown"
                    ref={trendDropdownRef}
                  >
                    <button
                      type="button"
                      className={`secondary-button ${
                        trendMenuOpen
                          ? "open"
                          : ""
                      }`}
                      onClick={() =>
                        setTrendMenuOpen(
                          (previous) =>
                            !previous
                        )
                      }
                    >
                      {trendRange}

                      <ChevronDown size={14} />
                    </button>

                    {trendMenuOpen && (
                      <div className="dropdown-menu trend-menu">
                        <div className="dropdown-heading">
                          Time window
                        </div>

                        {[
                          "7 Days",
                          "14 Days",
                          "30 Days",
                        ].map((option) => (
                          <button
                            type="button"
                            key={option}
                            className={
                              option ===
                              trendRange
                                ? "dropdown-selected"
                                : ""
                            }
                            onClick={() => {
                              setTrendRange(
                                option
                              );
                              setTrendMenuOpen(
                                false
                              );
                            }}
                          >
                            <span>
                              {option}
                            </span>

                            {option ===
                              trendRange && (
                              <CheckCircle2
                                size={14}
                              />
                            )}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                <div className="chart-container">
                  {trendLoading ? (
                    <div className="chart-loading">
                      Loading fraud trend...
                    </div>
                  ) : trendError ? (
                    <div className="chart-loading">
                      {trendError}
                    </div>
                  ) : (
                    <ResponsiveContainer
                      width="100%"
                      height="100%"
                    >
                      <AreaChart
                        data={trendData}
                      >
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
                  )}
                </div>
              </section>

              {/* Compact Network Intelligence */}

              <div>
                <NetworkIntelligenceSummary
                  dashboardData={
                    dashboardData
                  }
                  networkOverview={
                    networkOverview
                  }
                  networkLoading={
                    networkLoading
                  }
                  networkError={
                    networkError
                  }
                  onNavigate={
                    scrollToSection
                  }
                />
              </div>

              {/* Transactions */}

              <div
                ref={transactionsRef}
                id="transactions-section"
              >
                <RecentTransactions
                  transactions={
                    recentTransactions
                  }
                  onSelectTransaction={
                    handleSelectTransaction
                  }
                  showAll={
                    showAllTransactions
                  }
                  setShowAll={
                    setShowAllTransactions
                  }
                />
              </div>

              {/* Distribution */}

              <RiskDistribution
                dashboardData={dashboardData}
              />
            </div>

            {/* =================================================
                SECONDARY INTELLIGENCE
            ================================================= */}

            <div className="secondary-sections">
              <div
                ref={policiesRef}
                id="policies-section"
              >
                <PoliciesSection />
              </div>

              <div
                ref={alertsRef}
                id="alerts-section"
              >
                <AlertsSection
                  dashboardData={
                    dashboardData
                  }
                  onNavigate={
                    scrollToSection
                  }
                />
              </div>

              <div
                ref={reportsRef}
                id="reports-section"
              >
                <ReportsSection
                  dashboardData={
                    dashboardData
                  }
                />
              </div>

              <div
                ref={settingsRef}
                id="settings-section"
              >
                <SettingsSection />
              </div>
            </div>

            {/* =================================================
                RISK INSIGHTS
            ================================================= */}

            <RiskInsights
              dashboardData={dashboardData}
              onNavigate={scrollToSection}
            />
          </div>
        )}
      </main>

      {/* =====================================================
          INVESTIGATION OVERLAY
      ===================================================== */}

      <InvestigationPanel
        transaction={
          selectedTransaction
        }
        loading={
          investigationLoading
        }
        error={
          investigationError
        }
        onClose={
          closeInvestigation
        }
        mlScore={mlScore}
        mlLoading={mlLoading}
        mlError={mlError}
      />
    </div>
  );
}

export default Dashboard;