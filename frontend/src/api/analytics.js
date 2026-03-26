import api from './client'

export const fetchDashboard = async () => (await api.get('/analytics/dashboard')).data
export const fetchRfmHeatmap = async () => (await api.get('/analytics/rfm-heatmap')).data
export const fetchClusterScatter = async (limit = 3000) =>
	(await api.get(`/analytics/cluster-scatter?limit=${limit}`)).data
export const fetchRevenueBySegment = async () => (await api.get('/analytics/revenue-by-segment')).data
export const fetchRetentionCohort = async () => (await api.get('/analytics/retention-cohort')).data
export const fetchModelComparison = async () => (await api.get('/analytics/model-comparison')).data
