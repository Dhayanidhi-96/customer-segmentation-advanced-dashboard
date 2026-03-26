import { useState } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { fetchCustomerById, segmentCustomer } from '../api/customers'
import CustomerCard from '../components/ui/CustomerCard'
import SegmentBadge from '../components/ui/SegmentBadge'
import { useCustomers } from '../hooks/useCustomers'
import { formatCurrencyCompactIndian } from '../utils/numberFormat'

function Customers() {
  const [search, setSearch] = useState('')
  const [selected, setSelected] = useState(null)
  const { data = [], refetch } = useCustomers()

  const segmentMutation = useMutation({
    mutationFn: (customerId) => segmentCustomer({ customer_id: customerId, recalculate: true }),
    onSuccess: () => refetch(),
  })

  const customerDetail = useQuery({
    queryKey: ['customer-detail', selected],
    queryFn: () => fetchCustomerById(selected),
    enabled: Boolean(selected),
  })

  const filtered = data.filter((c) =>
    `${c.name} ${c.email} ${c.segment_label || ''}`.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="grid lg:grid-cols-[1fr_380px] gap-4">
      <div className="space-y-3">
        <input
          className="w-full rounded-lg border px-3 py-2"
          value={search}
          placeholder="Search by name, email, segment"
          onChange={(e) => setSearch(e.target.value)}
        />
        <div className="grid sm:grid-cols-2 gap-3">
          {filtered.map((customer) => (
            <div key={customer.id} onClick={() => setSelected(customer.id)}>
              <CustomerCard customer={customer} onResegment={(id) => segmentMutation.mutate(id)} />
            </div>
          ))}
        </div>
      </div>

      <aside className="bg-white border border-zinc-100 rounded-2xl p-4">
        <h3 className="font-display text-xl mb-2">Customer Detail</h3>
        {!selected && <p className="text-sm text-zinc-500">Select a customer to inspect order and segment history.</p>}
        {customerDetail.data && (
          <div className="space-y-3 text-sm">
            <div>
              <p className="font-semibold">{customerDetail.data.name}</p>
              <p className="text-zinc-500">{customerDetail.data.email}</p>
            </div>
            <div>
              <p className="font-semibold mb-1">Segment History</p>
              <div className="space-y-1">
                {customerDetail.data.segment_history.slice(0, 6).map((s, i) => (
                  <div key={i} className="flex items-center justify-between">
                    <SegmentBadge label={s.segment_label} />
                    <span>RFM {s.rfm_total_score}</span>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <p className="font-semibold mb-1">Recent Orders</p>
              <div className="max-h-56 overflow-auto space-y-1">
                {customerDetail.data.orders.slice(0, 12).map((o) => (
                  <div key={o.id} className="text-xs border rounded p-2">
                    {o.order_number} | {formatCurrencyCompactIndian(o.amount)} | {o.status}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </aside>
    </div>
  )
}

export default Customers
