import { useMemo, useState } from 'react'

import Card from '../components/Card'
import DataTable from '../components/DataTable'
import { Field, SelectField, TextAreaField } from '../components/Field'
import { pretty } from '../api'

const DATASETS = {
  ideas: { endpoint: '/api/v1/reference-data/ideas', defaultPath: 'data/input/ideas.csv', keyColumn: 'ID' },
  ra: { endpoint: '/api/v1/reference-data/ra-weights', defaultPath: 'data/input/weights_ra.csv', keyColumn: 'RequestingArea' },
  rs: { endpoint: '/api/v1/reference-data/rs-weights', defaultPath: 'data/input/weights_rs.csv', keyColumn: 'RevenueStream' }
}

export default function CrudView({ api, configPath }) {
  const [dataset, setDataset] = useState('ideas')
  const [path, setPath] = useState(DATASETS.ideas.defaultPath)
  const [limit, setLimit] = useState('50')
  const [offset, setOffset] = useState('0')
  const [rows, setRows] = useState([])
  const [total, setTotal] = useState(0)
  const [keyColumn, setKeyColumn] = useState(DATASETS.ideas.keyColumn)
  const [keyValue, setKeyValue] = useState('')
  const [rowJson, setRowJson] = useState('{\n  "ID": "",\n  "Name": ""\n}')
  const [overwriteJson, setOverwriteJson] = useState('[\n  {\n  }\n]')
  const [responseText, setResponseText] = useState('')
  const [busy, setBusy] = useState(false)

  const datasetOptions = useMemo(() => Object.keys(DATASETS), [])

  function onDatasetChange(next) {
    setDataset(next)
    setPath(DATASETS[next].defaultPath)
    setKeyColumn(DATASETS[next].keyColumn)
    setRows([])
    setTotal(0)
  }

  async function loadRows() {
    setBusy(true)
    try {
      const endpoint = DATASETS[dataset].endpoint
      const query = `?path=${encodeURIComponent(path)}&limit=${encodeURIComponent(limit)}&offset=${encodeURIComponent(offset)}${configPath ? `&config_path=${encodeURIComponent(configPath)}` : ''}`
      const data = await api.get(`${endpoint}${query}`)
      setRows(data.rows || [])
      setTotal(data.total || 0)
      setResponseText(pretty(data))
    } catch (error) {
      setResponseText(String(error))
    } finally {
      setBusy(false)
    }
  }

  async function upsertRow() {
    setBusy(true)
    try {
      const row = JSON.parse(rowJson)
      const payload = {
        path,
        key_column: keyColumn,
        row,
        ...(configPath ? { config_path: configPath } : {})
      }
      const data = await api.post('/api/v1/reference-data/upsert', payload)
      setResponseText(pretty(data))
    } catch (error) {
      setResponseText(String(error))
    } finally {
      setBusy(false)
    }
  }

  async function deleteRow() {
    setBusy(true)
    try {
      const payload = {
        path,
        key_column: keyColumn,
        key_value: keyValue,
        ...(configPath ? { config_path: configPath } : {})
      }
      const data = await api.post('/api/v1/reference-data/delete', payload)
      setResponseText(pretty(data))
    } catch (error) {
      setResponseText(String(error))
    } finally {
      setBusy(false)
    }
  }

  async function overwriteRows() {
    setBusy(true)
    try {
      const rowsPayload = JSON.parse(overwriteJson)
      const payload = {
        path,
        rows: rowsPayload,
        ...(configPath ? { config_path: configPath } : {})
      }
      const data = await api.post('/api/v1/reference-data/overwrite', payload)
      setResponseText(pretty(data))
    } catch (error) {
      setResponseText(String(error))
    } finally {
      setBusy(false)
    }
  }

  function editRow(row) {
    setRowJson(pretty(row))
    if (row[keyColumn] !== undefined) {
      setKeyValue(String(row[keyColumn]))
    }
  }

  return (
    <div className="stack">
      <Card title="CSV CRUD" subtitle="Read, upsert, delete, and overwrite rows for ideas/RA/RS datasets.">
        <div className="grid two">
          <SelectField label="Dataset" value={dataset} onChange={onDatasetChange} options={datasetOptions} />
          <Field label="CSV Path" value={path} onChange={setPath} />
        </div>
        <p className="note">Config Path: {configPath || '(none)'}</p>
        <div className="grid three">
          <Field label="Limit" value={limit} onChange={setLimit} type="number" />
          <Field label="Offset" value={offset} onChange={setOffset} type="number" />
          <button className="btn" disabled={busy} onClick={loadRows}>{busy ? 'Running...' : 'Load Rows'}</button>
        </div>

        <div className="grid two top-gap">
          <div>
            <Field label="Key Column" value={keyColumn} onChange={setKeyColumn} />
            <Field label="Key Value (for delete)" value={keyValue} onChange={setKeyValue} />
            <TextAreaField label="Upsert Row JSON" value={rowJson} onChange={setRowJson} rows={10} />
            <div className="actions">
              <button className="btn" disabled={busy} onClick={upsertRow}>Upsert</button>
              <button className="btn danger" disabled={busy} onClick={deleteRow}>Delete</button>
            </div>
          </div>
          <div>
            <TextAreaField label="Overwrite JSON Array" value={overwriteJson} onChange={setOverwriteJson} rows={10} />
            <button className="btn warning" disabled={busy} onClick={overwriteRows}>Overwrite Dataset</button>
            <p className="note">Total loaded rows: {total}</p>
          </div>
        </div>
      </Card>

      <Card title="Rows Preview">
        <DataTable rows={rows} onEdit={editRow} />
      </Card>

      <Card title="API Response">
        <pre className="result">{responseText || 'No response yet.'}</pre>
      </Card>
    </div>
  )
}
