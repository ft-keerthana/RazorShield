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

const transactions = [
  {
    id: "txn_955728888081",
    amount: "$1,171.95",
    customer: "cust_fc81df20a609",
    score: "0.05",
    decision: "ALLOW",
    risk: "low",
    time: "2 mins ago",
  },
  {
    id: "txn_4199ef5ba33c",
    amount: "$299.18",
    customer: "cust_193b89fd05b6",
    score: "0.42",
    decision: "REVIEW",
    risk: "medium",
    time: "5 mins ago",
  },
  {
    id: "txn_d943d97a1875",
    amount: "$46.67",
    customer: "cust_4102be1bcb53",
    score: "0.02",
    decision: "ALLOW",
    risk: "low",
    time: "8 mins ago",
  },
  {
    id: "txn_c22702e86ec4",
    amount: "$312.27",
    customer: "cust_214456f685e0",
    score: "0.31",
    decision: "REVIEW",
    risk: "medium",
    time: "12 mins ago",
  },
  {
    id: "txn_17571e32b758",
    amount: "$67.55",
    customer: "cust_1f9e9d6d4f13",
    score: "0.01",
    decision: "ALLOW",
    risk: "low",
    time: "15 mins ago",
  },
];

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

function StatCard({
  icon,
  title,
  value,
  description,
  variant = "purple",
}) {
  return (
    <div className="stat-card">
      <div className={`stat-icon ${variant}`}>{icon}</div>

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

function NetworkIntelligence() {
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

          <span className="network-status safe">No Spike</span>
        </div>

        <div className="network-item">
          <div className="network-icon purple">
            <GitBranch size={17} />
          </div>

          <div className="network-label">
            <strong>Abuse Network</strong>
            <span>Candidate network detection</span>
          </div>

          <span className="network-status warning">Detected</span>
        </div>

        <div className="network-item">
          <div className="network-icon blue">
            <Users size={17} />
          </div>

          <div className="network-label">
            <strong>Shared Devices</strong>
            <span>Entities sharing devices</span>
          </div>

          <strong className="network-number">998</strong>
        </div>

        <div className="network-item">
          <div className="network-icon blue">
            <Network size={17} />
          </div>

          <div className="network-label">
            <strong>Shared IPs</strong>
            <span>Entities sharing IP addresses</span>
          </div>

          <strong className="network-number">947</strong>
        </div>
      </div>

      <button className="primary-button">
        <Network size={16} />
        View Network Intelligence
      </button>
    </section>
  );
}

function RiskDistribution() {
  return (
    <section className="card distribution-card">
      <div className="card-header">
        <div>
          <h2>Risk Distribution</h2>
          <p>Transaction risk classification</p>
        </div>
      </div>

      <div className="distribution">
        <div className="donut">
          <div className="donut-center">
            <strong>10,000</strong>
            <span>Total</span>
          </div>
        </div>

        <div className="legend">
          <div className="legend-item">
            <span className="legend-dot green" />
            <div>
              <strong>Low Risk</strong>
              <span>6,430 · 64.3%</span>
            </div>
          </div>

          <div className="legend-item">
            <span className="legend-dot orange" />
            <div>
              <strong>Medium Risk</strong>
              <span>3,258 · 32.6%</span>
            </div>
          </div>

          <div className="legend-item">
            <span className="legend-dot red" />
            <div>
              <strong>High Risk</strong>
              <span>312 · 3.1%</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function RecentTransactions() {
  return (
    <section className="card transactions-card">
      <div className="card-header">
        <div>
          <h2>Recent Transactions</h2>
          <p>Latest transactions evaluated by RazorSentry</p>
        </div>

        <button className="secondary-button">View All</button>
      </div>

      <div className="transaction-table-wrapper">
        <table>
          <thead>
            <tr>
              <th>TRANSACTION ID</th>
              <th>AMOUNT</th>
              <th>CUSTOMER</th>
              <th>RISK SCORE</th>
              <th>DECISION</th>
              <th>TIME</th>
            </tr>
          </thead>

          <tbody>
            {transactions.map((transaction) => (
              <tr key={transaction.id}>
                <td>
                  <div className="transaction-id">
                    <span className={`risk-dot ${transaction.risk}`} />
                    {transaction.id}
                  </div>
                </td>

                <td className="amount">{transaction.amount}</td>

                <td className="customer">
                  {transaction.customer}
                </td>

                <td>
                  <span className={`score ${transaction.risk}`}>
                    {transaction.score}
                  </span>
                </td>

                <td>
                  <span
                    className={`decision ${transaction.decision.toLowerCase()}`}
                  >
                    {transaction.decision}
                  </span>
                </td>

                <td className="time">{transaction.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function Dashboard() {
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
              value="10,000"
              description="Dataset transactions"
              variant="purple"
            />

            <StatCard
              icon={<Activity size={21} />}
              title="Fraud Rate"
              value="2.91%"
              description="291 flagged as fraud"
              variant="red"
            />

            <StatCard
              icon={<Network size={21} />}
              title="Network Risk Score"
              value="60 / 100"
              description="Medium network risk"
              variant="blue"
            />

            <StatCard
              icon={<BarChart3 size={21} />}
              title="Transaction Volume"
              value="$2.81M"
              description="Average $280.56"
              variant="green"
            />

            <StatCard
              icon={<AlertTriangle size={21} />}
              title="Fraud Transactions"
              value="291"
              description="2.91% of transactions"
              variant="orange"
            />
          </div>

          <div className="dashboard-grid">
            <section className="card chart-card">
              <div className="card-header">
                <div>
                  <h2>Fraud Rate Trend</h2>
                  <p>Recent fraud activity across the monitoring window</p>
                </div>

                <button className="secondary-button">
                  7 Days
                  <ChevronDown size={14} />
                </button>
              </div>

              <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
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
                      tick={{ fill: "#6B7280", fontSize: 12 }}
                    />

                    <YAxis
                      domain={[0, 5]}
                      tickFormatter={(value) => `${value}%`}
                      axisLine={false}
                      tickLine={false}
                      tick={{ fill: "#6B7280", fontSize: 12 }}
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

            <NetworkIntelligence />

            <RecentTransactions />

            <RiskDistribution />
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
                  <strong>Candidate abuse network detected</strong>
                  <span>
                    Network intelligence identified suspicious
                    entity relationships.
                  </span>
                </div>
                <button>View</button>
              </div>

              <div className="insight-item">
                <span className="insight-marker orange" />
                <div>
                  <strong>Multiple risk signals active</strong>
                  <span>
                    Review transactions with elevated behavioral
                    risk.
                  </span>
                </div>
                <button>View</button>
              </div>

              <div className="insight-item">
                <span className="insight-marker purple" />
                <div>
                  <strong>Network monitoring operational</strong>
                  <span>
                    No current fraud spike detected.
                  </span>
                </div>
                <button>View</button>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;