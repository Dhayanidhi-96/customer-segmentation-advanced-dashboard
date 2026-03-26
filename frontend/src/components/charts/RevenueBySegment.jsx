import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { formatCurrencyCompactIndian } from '../../utils/numberFormat'

function RevenueBySegment({ data = [] }) {
  return (
    <div className="bg-white rounded-2xl p-4 border border-zinc-100">
      <h3 className="font-display mb-2">Revenue by Segment</h3>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" tickFormatter={(value) => formatCurrencyCompactIndian(value)} />
            <YAxis type="category" dataKey="segment" width={100} />
            <Tooltip formatter={(value) => formatCurrencyCompactIndian(value)} />
            <Bar dataKey="revenue" fill="#f06b4f" radius={[0, 6, 6, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default RevenueBySegment
