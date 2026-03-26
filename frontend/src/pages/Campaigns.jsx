import { useState } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { fetchCampaigns, triggerCampaign } from '../api/emails'
import EmailPreviewModal from '../components/ui/EmailPreviewModal'
import { formatDecimal } from '../utils/numberFormat'

const campaignTypes = ['vip_discount', 'winback', 'upsell', 'rfm_personalized']

function Campaigns() {
  const [preview, setPreview] = useState({ open: false, subject: '', html: '' })
  const campaigns = useQuery({
    queryKey: ['campaigns'],
    queryFn: fetchCampaigns,
    refetchInterval: 10000,
    refetchOnWindowFocus: false,
  })
  const trigger = useMutation({
    mutationFn: triggerCampaign,
    onSuccess: () => campaigns.refetch(),
  })

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-2xl p-4 border border-zinc-100">
        <h3 className="font-display text-2xl mb-3">Campaign Manager</h3>
        <div className="flex flex-wrap gap-2">
          {campaignTypes.map((type) => (
            <button
              key={type}
              className="px-3 py-2 rounded-lg bg-ink text-cream text-sm disabled:opacity-50"
              disabled={trigger.isPending}
              onClick={() => trigger.mutate(type)}
            >
              {trigger.isPending ? 'Triggering...' : `Trigger ${type}`}
            </button>
          ))}
        </div>
        {trigger.isSuccess && (
          <p className="text-xs text-emerald-700 mt-2">
            Campaign queued. Task ID: {trigger.data?.task_id || 'N/A'}
          </p>
        )}
        {trigger.isError && (
          <p className="text-xs text-red-600 mt-2">
            Failed to trigger campaign. Check backend/worker logs.
          </p>
        )}
        <p className="text-sm text-zinc-500 mt-3">
          Open rate: {formatDecimal(campaigns.data?.stats?.open_rate || 0, 1)}% | Click rate: {formatDecimal(campaigns.data?.stats?.click_rate || 0, 1)}%
        </p>
      </div>

      <div className="bg-white rounded-2xl p-4 border border-zinc-100 overflow-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr>
              <th className="p-2 text-left">Campaign</th>
              <th className="p-2 text-left">Subject</th>
              <th className="p-2 text-left">Status</th>
              <th className="p-2 text-left">Sent</th>
              <th className="p-2 text-left">Action</th>
            </tr>
          </thead>
          <tbody>
            {(campaigns.data?.data || []).length === 0 && (
              <tr>
                <td className="p-3 text-zinc-500" colSpan={5}>No campaign runs yet. Trigger one above and wait 5-15 seconds.</td>
              </tr>
            )}
            {(campaigns.data?.data || []).map((c) => (
              <tr key={c.id}>
                <td className="p-2">{c.campaign_type}</td>
                <td className="p-2">{c.subject}</td>
                <td className="p-2">{c.status}</td>
                <td className="p-2">{c.sent_at ? new Date(c.sent_at).toLocaleString() : '-'}</td>
                <td className="p-2">
                  <button
                    className="text-coral"
                    onClick={() =>
                      setPreview({
                        open: true,
                        subject: c.subject,
                        html: '<p>Email body is generated server-side at send-time.</p>',
                      })
                    }
                  >
                    Preview
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <EmailPreviewModal open={preview.open} onClose={() => setPreview((p) => ({ ...p, open: false }))} subject={preview.subject} html={preview.html} />
    </div>
  )
}

export default Campaigns
