import { formatCompactIndian } from '../../utils/numberFormat'

function RFMHeatmap({ data = [] }) {
  const max = Math.max(...data.map((d) => d.count), 1)
  return (
    <div className="bg-white rounded-2xl p-4 border border-zinc-100">
      <h3 className="font-display mb-3">RFM Heatmap (R/F)</h3>
      <div className="grid grid-cols-5 gap-2">
        {Array.from({ length: 25 }).map((_, idx) => {
          const r = Math.floor(idx / 5) + 1
          const f = (idx % 5) + 1
          const cell = data.find((d) => d.recency === r && d.frequency === f)
          const count = cell?.count || 0
          const opacity = count / max
          return (
            <div key={`${r}-${f}`} className="rounded-lg h-12 flex items-center justify-center text-xs" style={{ backgroundColor: `rgba(79,124,85,${0.12 + opacity * 0.88})`, color: '#111' }}>
              {formatCompactIndian(count, 1)}
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default RFMHeatmap
