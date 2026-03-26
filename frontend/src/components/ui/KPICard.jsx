function KPICard({ title, value, subtitle, helper }) {
  return (
    <div className="bg-white rounded-2xl p-5 border border-zinc-100 shadow-sm">
      <p className="text-xs uppercase tracking-wider text-zinc-500">{title}</p>
      <p className="text-3xl font-display mt-2">{value}</p>
      <p className="text-sm text-zinc-500 mt-1">{subtitle}</p>
      {helper && <p className="text-xs text-zinc-400 mt-1">{helper}</p>}
    </div>
  )
}

export default KPICard
