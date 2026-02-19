import { useState } from 'react'

import Card from '../components/Card'
import { Field } from '../components/Field'
import { pretty } from '../api'

export default function EntitiesView({ api, paths, configPath }) {
  const [raOld, setRaOld] = useState('')
  const [raNew, setRaNew] = useState('')
  const [rsOld, setRsOld] = useState('')
  const [rsNew, setRsNew] = useState('')
  const [responseText, setResponseText] = useState('')
  const [busy, setBusy] = useState(false)

  async function listRequestingAreas() {
    setBusy(true)
    try {
      const payload = {
        ideas_path: paths.ideas,
        ra_weights_path: paths.ra,
        ...(configPath ? { config_path: configPath } : {})
      }
      const data = await api.post('/api/v1/reference-data/requesting-areas/list', payload)
      setResponseText(pretty(data))
    } catch (error) {
      setResponseText(String(error))
    } finally {
      setBusy(false)
    }
  }

  async function renameRequestingArea() {
    setBusy(true)
    try {
      const payload = {
        ideas_path: paths.ideas,
        ra_weights_path: paths.ra,
        old_value: raOld,
        new_value: raNew,
        ...(configPath ? { config_path: configPath } : {})
      }
      const data = await api.post('/api/v1/reference-data/requesting-areas/rename', payload)
      setResponseText(pretty(data))
    } catch (error) {
      setResponseText(String(error))
    } finally {
      setBusy(false)
    }
  }

  async function listRevenueStreams() {
    setBusy(true)
    try {
      const payload = {
        ideas_path: paths.ideas,
        ra_weights_path: paths.ra,
        rs_weights_path: paths.rs,
        ...(configPath ? { config_path: configPath } : {})
      }
      const data = await api.post('/api/v1/reference-data/revenue-streams/list', payload)
      setResponseText(pretty(data))
    } catch (error) {
      setResponseText(String(error))
    } finally {
      setBusy(false)
    }
  }

  async function renameRevenueStream() {
    setBusy(true)
    try {
      const payload = {
        ideas_path: paths.ideas,
        ra_weights_path: paths.ra,
        rs_weights_path: paths.rs,
        old_value: rsOld,
        new_value: rsNew,
        ...(configPath ? { config_path: configPath } : {})
      }
      const data = await api.post('/api/v1/reference-data/revenue-streams/rename', payload)
      setResponseText(pretty(data))
    } catch (error) {
      setResponseText(String(error))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="stack">
      <Card title="Entity Tools" subtitle="List and rename Requesting Areas and Revenue Streams across related files.">
        <div className="grid two">
          <div>
            <h3>Requesting Areas</h3>
            <div className="actions">
              <button className="btn" disabled={busy} onClick={listRequestingAreas}>List</button>
            </div>
            <Field label="Old Value" value={raOld} onChange={setRaOld} />
            <Field label="New Value" value={raNew} onChange={setRaNew} />
            <button className="btn" disabled={busy} onClick={renameRequestingArea}>Rename Requesting Area</button>
          </div>

          <div>
            <h3>Revenue Streams</h3>
            <div className="actions">
              <button className="btn" disabled={busy} onClick={listRevenueStreams}>List</button>
            </div>
            <Field label="Old Value" value={rsOld} onChange={setRsOld} />
            <Field label="New Value" value={rsNew} onChange={setRsNew} />
            <button className="btn" disabled={busy} onClick={renameRevenueStream}>Rename Revenue Stream</button>
          </div>
        </div>
      </Card>

      <Card title="API Response">
        <pre className="result">{responseText || 'No response yet.'}</pre>
      </Card>
    </div>
  )
}
