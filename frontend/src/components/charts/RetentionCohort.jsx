function RetentionCohort({ data = [] }) {
  const months = Array.from(new Set(data.flatMap((c) => Object.keys(c.values || {})))).sort()
  return (
    <div className="bg-white rounded-2xl p-4 border border-zinc-100 overflow-auto">
      <h3 className="font-display mb-2">Retention Cohort</h3>
      <table className="min-w-full text-sm">
        <thead>
          <tr>
            <th className="text-left p-2">Cohort</th>
            {months.map((m) => (
              <th key={m} className="text-left p-2">{m}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.cohort}>
              <td className="p-2 font-semibold">{row.cohort}</td>
              {months.map((m) => {
                const v = row.values?.[m] || 0
                return <td key={m} className="p-2">{v}</td>
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default RetentionCohort
