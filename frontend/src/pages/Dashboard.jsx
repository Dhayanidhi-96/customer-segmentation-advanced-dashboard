import { useSegments } from '../hooks/useSegments'
import { useAnalytics } from '../hooks/useAnalytics'
import ClusterScatterPlot from '../components/charts/ClusterScatterPlot'
import RFMHeatmap from '../components/charts/RFMHeatmap'
import RevenueBySegment from '../components/charts/RevenueBySegment'
import SegmentPieChart from '../components/charts/SegmentPieChart'
import KPICard from '../components/ui/KPICard'
import { formatCompactIndian, formatCurrencyCompactIndian, formatIndianNumber } from '../utils/numberFormat'

function Dashboard() {
  const { data: segments } = useSegments()
  const { dashboard, heatmap, scatter, revenue } = useAnalytics()

  const d = dashboard.data || {
    total_customers: 0,
    revenue_this_month: 0,
    avg_rfm_score: 0,
    email_open_rate: 0,
  }

  return (
    <div className="space-y-4 md:space-y-6">
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Total Customers"
          value={`${formatCompactIndian(d.total_customers)} customers`}
          subtitle="Current active base"
          helper={`${formatIndianNumber(d.total_customers)} customers`}
        />
        <KPICard
          title="Revenue This Month"
          value={formatCurrencyCompactIndian(d.revenue_this_month)}
          subtitle="Gross completed orders"
          helper={`₹${formatIndianNumber(d.revenue_this_month)}`}
        />
        <KPICard
          title="Avg RFM Score"
          value={Number(d.avg_rfm_score).toFixed(2)}
          subtitle="RFM score (max 15)"
          helper="R=Recency(days), F=Frequency, M=Monetary"
        />
        <KPICard title="Email Open Rate" value={`${Number(d.email_open_rate).toFixed(1)}%`} subtitle="Campaign engagement" />
      </div>

      <div className="grid lg:grid-cols-2 gap-4">
        <SegmentPieChart data={segments || []} />
        <RFMHeatmap data={heatmap.data?.data || []} />
        <RevenueBySegment data={revenue.data?.data || []} />
        <ClusterScatterPlot data={scatter.data?.data || []} />
      </div>
    </div>
  )
}

export default Dashboard
