import { useQuery } from '@tanstack/react-query'
import { fetchCustomers } from '../api/customers'

export const useCustomers = () => {
  return useQuery({
    queryKey: ['customers'],
    queryFn: fetchCustomers,
    staleTime: 5 * 60 * 1000,
    gcTime: 15 * 60 * 1000,
    refetchOnWindowFocus: false,
  })
}
