import { useQuery } from '@tanstack/react-query'
import {
  fetchClusterScatter,
  fetchDashboard,
  fetchRevenueBySegment,
  fetchRfmHeatmap,
} from '../api/analytics'

export const useAnalytics = () => {
  const commonOptions = {
    staleTime: 5 * 60 * 1000,
    gcTime: 15 * 60 * 1000,
    refetchOnWindowFocus: false,
  }

  const dashboard = useQuery({ queryKey: ['dashboard'], queryFn: fetchDashboard, ...commonOptions })
  const heatmap = useQuery({ queryKey: ['rfm-heatmap'], queryFn: fetchRfmHeatmap, ...commonOptions })
  const scatter = useQuery({ queryKey: ['cluster-scatter'], queryFn: () => fetchClusterScatter(3000), ...commonOptions })
  const revenue = useQuery({ queryKey: ['revenue-segment'], queryFn: fetchRevenueBySegment, ...commonOptions })

  return { dashboard, heatmap, scatter, revenue }
}
