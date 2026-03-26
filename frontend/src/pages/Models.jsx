import { useState } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { fetchModelComparison } from '../api/analytics'
import ModelComparisonChart from '../components/charts/ModelComparisonChart'
import { fetchBestModel, fetchModels, retrainModels } from '../api/models'
import { formatCompactIndian, formatDecimal } from '../utils/numberFormat'

function Models() {
  const [chartMode, setChartMode] = useState('normalized')
  const models = useQuery({ queryKey: ['models-list'], queryFn: fetchModels })
  const best = useQuery({ queryKey: ['best-model'], queryFn: fetchBestModel })
  const comparison = useQuery({ queryKey: ['model-comparison'], queryFn: fetchModelComparison, staleTime: 5 * 60 * 1000 })
  const retrain = useMutation({ mutationFn: retrainModels, onSuccess: () => { models.refetch(); best.refetch() } })

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-2xl border border-zinc-100 p-4 flex items-center justify-between">
        <div>
          <h3 className="font-display text-2xl">Model Comparison</h3>
          <p className="text-sm text-zinc-500">Best model: {best.data?.data?.model_name || 'N/A'}</p>
        </div>
        <button className="px-4 py-2 rounded-lg bg-coral text-white" onClick={() => retrain.mutate()}>
          Retrain Models
        </button>
      </div>

      <div className="flex items-center gap-2">
        <button
          className={`px-3 py-1 rounded-lg text-sm ${chartMode === 'normalized' ? 'bg-ink text-cream' : 'bg-zinc-200 text-zinc-700'}`}
          onClick={() => setChartMode('normalized')}
        >
          Normalized
        </button>
        <button
          className={`px-3 py-1 rounded-lg text-sm ${chartMode === 'raw' ? 'bg-ink text-cream' : 'bg-zinc-200 text-zinc-700'}`}
          onClick={() => setChartMode('raw')}
        >
          Raw
        </button>
      </div>

      <ModelComparisonChart mode={chartMode} data={(comparison.data?.data || []).slice(0, 8)} />

      <div className="bg-white rounded-2xl border border-zinc-100 p-4 overflow-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr>
              <th className="p-2 text-left">Model</th>
              <th className="p-2 text-left">Silhouette</th>
              <th className="p-2 text-left">DBI</th>
              <th className="p-2 text-left">CH</th>
              <th className="p-2 text-left">Best</th>
              <th className="p-2 text-left">Trained</th>
            </tr>
          </thead>
          <tbody>
            {(models.data?.data || []).map((m) => (
              <tr key={m.id} className={m.is_best ? 'bg-amber-50' : ''}>
                <td className="p-2">{m.model_name}</td>
                <td className="p-2">{m.silhouette_score == null ? '-' : formatDecimal(m.silhouette_score, 3)}</td>
                <td className="p-2">{m.davies_bouldin_index == null ? '-' : formatDecimal(m.davies_bouldin_index, 3)}</td>
                <td className="p-2">{m.calinski_harabasz_score == null ? '-' : formatCompactIndian(m.calinski_harabasz_score)}</td>
                <td className="p-2">{m.is_best ? 'Yes' : 'No'}</td>
                <td className="p-2">{new Date(m.trained_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Models
