import { useMemo, useState } from 'react'

import { createApiClient } from './api'
import Sidebar from './components/Sidebar'
import CrudView from './views/CrudView'
import EntitiesView from './views/EntitiesView'
import JobsView from './views/JobsView'
import SettingsView from './views/SettingsView'
import WorkflowsView from './views/WorkflowsView'

export default function App() {
  const [activeTab, setActiveTab] = useState('crud')
  const [settings, setSettings] = useState({
    baseUrl: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
    apiKey: import.meta.env.VITE_API_KEY || '',
    role: import.meta.env.VITE_API_ROLE || 'admin',
    configPath: ''
  })
  const [paths, setPaths] = useState({
    ideas: 'data/input/ideas.csv',
    ra: 'data/input/weights_ra.csv',
    rs: 'data/input/weights_rs.csv'
  })

  const api = useMemo(() => createApiClient(settings), [settings])

  return (
    <div className="layout">
      <Sidebar active={activeTab} onChange={setActiveTab} />
      <div className="content">
        <header className="topbar">
          <div>
            <h2>Operational Dashboard</h2>
            <p>Inspired by CRUD admin layouts, adapted for TOM Demand workflows and data management.</p>
          </div>
        </header>

        {activeTab === 'crud' ? <CrudView api={api} configPath={settings.configPath} /> : null}
        {activeTab === 'entities' ? <EntitiesView api={api} paths={paths} configPath={settings.configPath} /> : null}
        {activeTab === 'workflows' ? <WorkflowsView api={api} paths={paths} configPath={settings.configPath} /> : null}
        {activeTab === 'jobs' ? <JobsView api={api} paths={paths} configPath={settings.configPath} /> : null}
        {activeTab === 'settings' ? (
          <SettingsView
            settings={settings}
            onSettingsChange={setSettings}
            paths={paths}
            onPathsChange={setPaths}
          />
        ) : null}
      </div>
    </div>
  )
}
