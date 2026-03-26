import api from './client'

export const fetchModels = async () => (await api.get('/models/list')).data
export const fetchBestModel = async () => (await api.get('/models/best')).data
export const retrainModels = async () => (await api.post('/models/retrain')).data
