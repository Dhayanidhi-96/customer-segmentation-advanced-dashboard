import { CartesianGrid, ResponsiveContainer, Scatter, ScatterChart, Tooltip, XAxis, YAxis } from 'recharts'

function ClusterScatterPlot({ data = [] }) {
  const points = data.slice(0, 3000)

  return (
    <div className="bg-white rounded-2xl p-4 border border-zinc-100">
      <h3 className="font-display mb-2">Cluster Scatter (PCA, sampled)</h3>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart>
            <CartesianGrid />
            <XAxis dataKey="x" type="number" name="PCA-1" />
            <YAxis dataKey="y" type="number" name="PCA-2" />
            <Tooltip cursor={{ strokeDasharray: '3 3' }} />
            <Scatter data={points} fill="#4f7c55" shape="circle" />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default ClusterScatterPlot
