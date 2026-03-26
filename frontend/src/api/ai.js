import api from './client'

export const askAI = async (payload) => (await api.post('/ai/chat', payload)).data
export const fetchRecommendations = async () => (await api.get('/ai/recommendations')).data
