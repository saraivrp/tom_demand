export default function Card({ title, subtitle, children }) {
  return (
    <section className="card">
      <header className="card-header">
        <h2>{title}</h2>
        {subtitle ? <p>{subtitle}</p> : null}
      </header>
      <div className="card-body">{children}</div>
    </section>
  )
}
