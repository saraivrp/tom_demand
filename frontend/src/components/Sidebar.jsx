const TABS = [
  { id: 'crud', label: 'CSV CRUD' },
  { id: 'entities', label: 'Entity Tools' },
  { id: 'workflows', label: 'Workflows' },
  { id: 'jobs', label: 'Async Jobs' },
  { id: 'settings', label: 'API Settings' }
]

export default function Sidebar({ active, onChange }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-dot" />
        <div>
          <h1>TOM Console</h1>
          <p>Demand Manager</p>
        </div>
      </div>

      <nav className="nav-list">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            className={`nav-item ${active === tab.id ? 'active' : ''}`}
            onClick={() => onChange(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </nav>
    </aside>
  )
}
