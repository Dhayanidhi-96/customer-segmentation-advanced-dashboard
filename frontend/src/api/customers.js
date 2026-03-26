import api from './client'

export const fetchCustomers = async () => (await api.get('/customers')).data
export const fetchCustomerById = async (id) => (await api.get(`/customers/${id}`)).data
export const segmentCustomer = async (payload) => (await api.post('/customers/segment', payload)).data
