import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { formatCompactIndian, formatDecimal } from '../../utils/numberFormat'

function ModelComparisonChart({ data = [], mode = 'normalized' }) {
  if (!data.length) {
    return (
      <div className="bg-white rounded-2xl p-4 border border-zinc-100">
        <h3 className="font-display mb-2">Model Comparison</h3>
        <div className="h-72 flex items-center justify-center text-sm text-zinc-500">No model comparison data</div>
      </div>
    )
  }

  const normalize = (arr, invert = false) => {
    const nums = arr.map((v) => Number(v ?? 0))
    const min = Math.min(...nums)
    const max = Math.max(...nums)
    if (max === min) return nums.map(() => 0.5)
    const norm = nums.map((v) => (v - min) / (max - min))
    return invert ? norm.map((v) => 1 - v) : norm
  }

  const silNorm = normalize(data.map((d) => d.silhouette_score ?? 0), false)
  const dbiNorm = normalize(data.map((d) => d.davies_bouldin_index ?? 0), true)
  const chNorm = normalize(data.map((d) => d.calinski_harabasz_score ?? 0), false)

  const chartData = data.map((row, idx) => ({
    ...row,
    silhouette_norm: Number(silNorm[idx].toFixed(3)),
    dbi_norm: Number(dbiNorm[idx].toFixed(3)),
    ch_norm: Number(chNorm[idx].toFixed(3)),
  }))

  const isRaw = mode === 'raw'

  return (
    <div className="bg-white rounded-2xl p-4 border border-zinc-100">
      <h3 className="font-display mb-2">Model Comparison ({isRaw ? 'Raw' : 'Normalized'})</h3>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="model_name" />
            <YAxis
              domain={isRaw ? [0, 'auto'] : [0, 1]}
              tickFormatter={(v) => (isRaw ? formatCompactIndian(v) : formatDecimal(v, 1))}
            />
            {isRaw ? (
              <Tooltip
                formatter={(value, name) => {
                  if (name === 'calinski_harabasz_score') return [formatCompactIndian(value), 'Calinski']
                  return [formatDecimal(value, 3), name]
                }}
              />
            ) : (
              <Tooltip
                formatter={(value, name, item) => {
                  const source = item?.payload || {}
                  if (name === 'silhouette_norm') return [`norm ${formatDecimal(value, 3)} | raw ${formatDecimal(source.silhouette_score, 3)}`, 'Silhouette']
                  if (name === 'dbi_norm') return [`norm ${formatDecimal(value, 3)} | raw ${formatDecimal(source.davies_bouldin_index, 3)}`, 'DBI (lower better)']
                  return [`norm ${formatDecimal(value, 3)} | raw ${formatCompactIndian(source.calinski_harabasz_score)}`, 'Calinski']
                }}
              />
            )}
            <Legend />
            {isRaw ? (
              <>
                <Bar dataKey="silhouette_score" fill="#4f7c55" name="Silhouette" />
                <Bar dataKey="davies_bouldin_index" fill="#f06b4f" name="DBI" />
                <Bar dataKey="calinski_harabasz_score" fill="#f7b538" name="Calinski" />
              </>
            ) : (
              <>
                <Bar dataKey="silhouette_norm" fill="#4f7c55" name="Silhouette" minPointSize={4} />
                <Bar dataKey="dbi_norm" fill="#f06b4f" name="DBI (inverted)" minPointSize={4} />
                <Bar dataKey="ch_norm" fill="#f7b538" name="Calinski" minPointSize={4} />
              </>
            )}
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default ModelComparisonChart
