export default function DataTable({ rows, onEdit }) {
  if (!rows || rows.length === 0) {
    return <div className="empty">No rows loaded.</div>
  }

  const columns = Array.from(rows.reduce((acc, row) => {
    Object.keys(row).forEach((key) => acc.add(key))
    return acc
  }, new Set()))

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Actions</th>
            {columns.map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx}>
              <td>
                <button className="btn small" onClick={() => onEdit(row)}>Edit</button>
              </td>
              {columns.map((column) => (
                <td key={column}>{String(row[column] ?? '')}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
