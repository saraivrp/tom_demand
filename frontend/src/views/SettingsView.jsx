import Card from '../components/Card'
import { Field, SelectField } from '../components/Field'

const ROLES = ['viewer', 'editor', 'executor', 'admin']

export default function SettingsView({ settings, onSettingsChange, paths, onPathsChange }) {
  return (
    <div className="stack">
      <Card title="API Settings" subtitle="Connection and auth headers used by all requests.">
        <div className="grid two">
          <Field label="Base URL" value={settings.baseUrl} onChange={(v) => onSettingsChange({ ...settings, baseUrl: v })} />
          <Field label="API Key" value={settings.apiKey} onChange={(v) => onSettingsChange({ ...settings, apiKey: v })} />
          <SelectField label="Role" value={settings.role} onChange={(v) => onSettingsChange({ ...settings, role: v })} options={ROLES} />
          <Field label="Config Path (optional)" value={settings.configPath} onChange={(v) => onSettingsChange({ ...settings, configPath: v })} />
        </div>
      </Card>

      <Card title="Default File Paths" subtitle="Used across CRUD, entity operations, workflows, and jobs.">
        <div className="grid one">
          <Field label="Ideas CSV" value={paths.ideas} onChange={(v) => onPathsChange({ ...paths, ideas: v })} />
          <Field label="RA Weights CSV" value={paths.ra} onChange={(v) => onPathsChange({ ...paths, ra: v })} />
          <Field label="RS Weights CSV" value={paths.rs} onChange={(v) => onPathsChange({ ...paths, rs: v })} />
        </div>
      </Card>
    </div>
  )
}
