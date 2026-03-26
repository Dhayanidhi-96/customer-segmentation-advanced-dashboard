import { useSegments } from '../hooks/useSegments'
import { formatCompactIndian, formatCurrencyCompactIndian, formatIndianNumber } from '../utils/numberFormat'

function Segments() {
  const { data = [] } = useSegments()

  return (
    <div className="bg-white rounded-2xl p-5 border border-zinc-100">
      <h3 className="font-display text-2xl mb-4">Segment Explorer</h3>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {data.map((segment) => (
          <div key={segment.segment_label} className="border rounded-xl p-4">
            <p className="text-sm text-zinc-500">{segment.segment_label}</p>
            <p className="text-3xl font-display">{formatCompactIndian(segment.customer_count)} customers</p>
            <p className="text-xs text-zinc-400">{formatIndianNumber(segment.customer_count)} customers</p>
            <p className="text-sm mt-2">Revenue: {formatCurrencyCompactIndian(segment.revenue)}</p>
            <p className="text-xs text-zinc-400">₹{formatIndianNumber(segment.revenue)}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Segments
