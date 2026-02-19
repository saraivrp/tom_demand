import { useRef, useState } from 'react'

import Card from '../components/Card'
import { Field, SelectField } from '../components/Field'
import { pretty } from '../api'

const METHODS = ['sainte-lague', 'dhondt', 'wsjf']
const OPTIONAL_METHODS = ['', ...METHODS]

export default function WorkflowsView({ api, paths, configPath }) {
  const [ideasPathOverride, setIdeasPathOverride] = useState('')
  const [method, setMethod] = useState('sainte-lague')
  const [nowMethod, setNowMethod] = useState('')
  const [nextMethod, setNextMethod] = useState('')
  const [laterMethod, setLaterMethod] = useState('')
  const [topN, setTopN] = useState('20')
  const [outputDir, setOutputDir] = useState('data/output')
  const [outputRs, setOutputRs] = useState('data/output/prioritization_rs.csv')
  const [outputGlobal, setOutputGlobal] = useState('data/output/demand.csv')
  const [outputCompare, setOutputCompare] = useState('data/output/comparison.csv')
  const [requestText, setRequestText] = useState('')
  const [responseText, setResponseText] = useState('')
  const [busy, setBusy] = useState(false)
  const ideasFileInputRef = useRef(null)
  const effectiveIdeasPath = ideasPathOverride.trim() || paths.ideas

  async function call(path, payload) {
    setRequestText(pretty({ path, payload }))
    setBusy(true)
    try {
      const data = await api.post(path, payload)
      setResponseText(pretty(data))
    } catch (error) {
      setResponseText(String(error))
    } finally {
      setBusy(false)
    }
  }

  async function uploadIdeasFile(event) {
    const file = event.target.files?.[0]
    event.target.value = ''
    if (!file) {
      return
    }

    setRequestText(pretty({
      path: '/api/v1/reference-data/upload-ideas',
      payload: { filename: file.name, size: file.size }
    }))
    setBusy(true)
    try {
      const data = await api.upload('/api/v1/reference-data/upload-ideas', 'file', file)
      setIdeasPathOverride(data.path)
      setResponseText(pretty(data))
    } catch (error) {
      setResponseText(String(error))
    } finally {
      setBusy(false)
    }
  }

  const basePayload = {
    ideas_path: effectiveIdeasPath,
    ra_weights_path: paths.ra,
    rs_weights_path: paths.rs,
    ...(configPath ? { config_path: configPath } : {})
  }

  const normalizeMethod = (value) => {
    const normalized = String(value || '').trim()
    return normalized || null
  }
  const hasQueueOverrides = Boolean(
    normalizeMethod(nowMethod) || normalizeMethod(nextMethod) || normalizeMethod(laterMethod)
  )

  const queueMethodsOnlyForPrioritizeMessage =
    'Queue-specific methods (NOW/NEXT/LATER) are only supported by "Prioritize". Clear those fields to use "Prioritize RS" or "Prioritize Global".'

  const buildPrioritizePayload = () => {
    const normalizedDefaultMethod = normalizeMethod(method) || 'sainte-lague'
    const normalizedNowMethod = normalizeMethod(nowMethod)
    const normalizedNextMethod = normalizeMethod(nextMethod)
    const normalizedLaterMethod = normalizeMethod(laterMethod)

    return {
      ...basePayload,
      output_dir: outputDir,
      method: normalizedDefaultMethod,
      ...(normalizedNowMethod ? { now_method: normalizedNowMethod } : {}),
      ...(normalizedNextMethod ? { next_method: normalizedNextMethod } : {}),
      ...(normalizedLaterMethod ? { later_method: normalizedLaterMethod } : {})
    }
  }

  return (
    <div className="stack">
      <Card title="Workflow Execution" subtitle="Run all exposed workflow endpoints from a single panel.">
        <div className="grid two">
          <Field
            label="Ideas File (override optional)"
            value={ideasPathOverride}
            onChange={setIdeasPathOverride}
            placeholder={paths.ideas}
          />
          <div className="align-end">
            <button className="btn" disabled={busy} onClick={() => ideasFileInputRef.current?.click()}>
              Browse Ideas CSV
            </button>
            <input
              ref={ideasFileInputRef}
              type="file"
              accept=".csv,text/csv"
              style={{ display: 'none' }}
              onChange={uploadIdeasFile}
            />
          </div>
          <SelectField label="Default Method (fallback)" value={method} onChange={setMethod} options={METHODS} />
          <SelectField label="NOW Method (optional — overrides Default)" value={nowMethod} onChange={setNowMethod} options={OPTIONAL_METHODS} />
          <SelectField label="NEXT Method (optional — overrides Default)" value={nextMethod} onChange={setNextMethod} options={OPTIONAL_METHODS} />
          <SelectField label="LATER Method (optional — overrides Default)" value={laterMethod} onChange={setLaterMethod} options={OPTIONAL_METHODS} />
          <Field label="Top N (compare)" value={topN} onChange={setTopN} type="number" />
          <Field label="Output Directory" value={outputDir} onChange={setOutputDir} />
          <Field label="Output RS" value={outputRs} onChange={setOutputRs} />
          <Field label="Output Global" value={outputGlobal} onChange={setOutputGlobal} />
          <Field label="Output Compare" value={outputCompare} onChange={setOutputCompare} />
        </div>
        <p>
          Queue-specific methods apply only to <strong>Prioritize</strong> (`/api/v1/workflows/prioritize`).
        </p>

        <div className="actions wrap">
          <button className="btn" disabled={busy} onClick={() => call('/api/v1/workflows/validate', basePayload)}>Validate</button>
          <button
            className="btn"
            disabled={busy}
            onClick={() => call('/api/v1/workflows/prioritize', buildPrioritizePayload())}
          >
            Prioritize
          </button>
          <button
            className="btn"
            disabled={busy || hasQueueOverrides}
            onClick={() => {
              if (hasQueueOverrides) {
                setResponseText(queueMethodsOnlyForPrioritizeMessage)
                return
              }
              call('/api/v1/workflows/prioritize-rs', {
                ideas_path: effectiveIdeasPath,
                ra_weights_path: paths.ra,
                output_path: outputRs,
                method,
                ...(configPath ? { config_path: configPath } : {})
              })
            }}
          >
            Prioritize RS
          </button>
          <button
            className="btn"
            disabled={busy || hasQueueOverrides}
            onClick={() => {
              if (hasQueueOverrides) {
                setResponseText(queueMethodsOnlyForPrioritizeMessage)
                return
              }
              call('/api/v1/workflows/prioritize-global', {
                rs_prioritized_path: outputRs,
                rs_weights_path: paths.rs,
                output_path: outputGlobal,
                method,
                ...(configPath ? { config_path: configPath } : {})
              })
            }}
          >
            Prioritize Global
          </button>
          <button
            className="btn"
            disabled={busy}
            onClick={() => call('/api/v1/workflows/compare', {
              ...basePayload,
              output_path: outputCompare,
              top_n: Number(topN || 0) || null
            })}
          >
            Compare Methods
          </button>
        </div>
      </Card>

      <Card title="API Request">
        <pre className="result">{requestText || 'No request yet.'}</pre>
      </Card>

      <Card title="API Response">
        <pre className="result">{responseText || 'No response yet.'}</pre>
      </Card>
    </div>
  )
}
