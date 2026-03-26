import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'
import { formatCompactIndian } from '../../utils/numberFormat'

const colors = ['#f7b538', '#4f7c55', '#f06b4f', '#3b82f6', '#6b7280', '#9333ea']

function SegmentPieChart({ data = [] }) {
  return (
    <div className="bg-white rounded-2xl p-4 border border-zinc-100">
      <h3 className="font-display mb-2">Segment Distribution</h3>
      <div className="h-72">
        {data.length === 0 ? (
          <div className="h-full flex items-center justify-center text-sm text-zinc-500">No segment data yet</div>
        ) : (
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={data} dataKey="customer_count" nameKey="segment_label" innerRadius={58} outerRadius={100}>
              {data.map((entry, index) => (
                <Cell key={entry.segment_label} fill={colors[index % colors.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => formatCompactIndian(value)} />
          </PieChart>
        </ResponsiveContainer>
        )}
      </div>
    </div>
  )
}

export default SegmentPieChart
