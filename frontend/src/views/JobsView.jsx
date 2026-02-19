import { useState } from 'react'

import Card from '../components/Card'
import { Field } from '../components/Field'
import { pretty } from '../api'

export default function JobsView({ api, paths, configPath }) {
  const [jobId, setJobId] = useState('')
  const [responseText, setResponseText] = useState('')
  const [busy, setBusy] = useState(false)

  async function submit(path, payload) {
    setBusy(true)
    try {
      const data = await api.post(path, payload)
      setResponseText(pretty(data))
      if (data.job_id) {
        setJobId(data.job_id)
      }
    } catch (error) {
      setResponseText(String(error))
    } finally {
      setBusy(false)
    }
  }

  async function listJobs() {
    setBusy(true)
    try {
      const data = await api.get('/api/v1/jobs?limit=20')
      setResponseText(pretty(data))
    } catch (error) {
      setResponseText(String(error))
    } finally {
      setBusy(false)
    }
  }

  async function getJob() {
    setBusy(true)
    try {
      const data = await api.get(`/api/v1/jobs/${encodeURIComponent(jobId)}`)
      setResponseText(pretty(data))
    } catch (error) {
      setResponseText(String(error))
    } finally {
      setBusy(false)
    }
  }

  const validatePayload = {
    ideas_path: paths.ideas,
    ra_weights_path: paths.ra,
    rs_weights_path: paths.rs,
    ...(configPath ? { config_path: configPath } : {})
  }

  return (
    <div className="stack">
      <Card title="Async Jobs" subtitle="Submit long operations and monitor execution status.">
        <div className="actions wrap">
          <button className="btn" disabled={busy} onClick={() => submit('/api/v1/jobs/workflows/validate', validatePayload)}>Submit Validate Job</button>
          <button
            className="btn"
            disabled={busy}
            onClick={() => submit('/api/v1/jobs/workflows/prioritize', {
              ...validatePayload,
              output_dir: '/tmp/tom_demand_jobs_output',
              method: 'sainte-lague'
            })}
          >
            Submit Prioritize Job
          </button>
          <button
            className="btn"
            disabled={busy}
            onClick={() => submit('/api/v1/jobs/workflows/compare', {
              ...validatePayload,
              output_path: '/tmp/tom_demand_jobs_output/compare.csv',
              top_n: 25
            })}
          >
            Submit Compare Job
          </button>
          <button className="btn" disabled={busy} onClick={listJobs}>List Jobs</button>
        </div>

        <div className="grid two">
          <Field label="Job ID" value={jobId} onChange={setJobId} />
          <div className="align-end">
            <button className="btn" disabled={busy || !jobId.trim()} onClick={getJob}>Get Job Status</button>
          </div>
        </div>
      </Card>

      <Card title="API Response">
        <pre className="result">{responseText || 'No response yet.'}</pre>
      </Card>
    </div>
  )
}
