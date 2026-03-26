import SegmentBadge from './SegmentBadge'

function CustomerCard({ customer, onResegment }) {
  return (
    <div className="bg-white p-4 rounded-xl border border-zinc-100">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-semibold">{customer.name}</h3>
          <p className="text-sm text-zinc-500">{customer.email}</p>
        </div>
        <SegmentBadge label={customer.segment_label || 'Unknown'} />
      </div>
      <div className="mt-3 text-sm text-zinc-600">RFM: {customer.rfm_total_score ?? '-'}</div>
      <button className="mt-3 px-3 py-2 bg-ink text-cream rounded-lg text-sm" onClick={() => onResegment(customer.id)}>
        Re-segment
      </button>
    </div>
  )
}

export default CustomerCard
