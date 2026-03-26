import api from './client'

export const fetchCampaigns = async () => (await api.get('/emails/campaigns')).data
export const triggerCampaign = async (campaignType) => (await api.post(`/emails/trigger/${campaignType}`)).data
