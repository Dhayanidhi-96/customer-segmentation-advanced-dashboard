const colorMap = {
  VIP: 'bg-amber-100 text-amber-700',
  Loyal: 'bg-moss/20 text-moss',
  'At-Risk': 'bg-red-100 text-red-700',
  New: 'bg-blue-100 text-blue-700',
  Churned: 'bg-zinc-200 text-zinc-700',
  Potential: 'bg-coral/20 text-coral',
  Outlier: 'bg-violet-100 text-violet-700',
}

function SegmentBadge({ label }) {
  return <span className={`px-2 py-1 rounded-full text-xs font-semibold ${colorMap[label] || 'bg-zinc-100 text-zinc-700'}`}>{label}</span>
}

export default SegmentBadge
