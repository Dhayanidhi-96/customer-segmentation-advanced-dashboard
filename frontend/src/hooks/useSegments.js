import { useQuery } from '@tanstack/react-query'
import api from '../api/client'

const fetchSegments = async () => (await api.get('/segments/summary')).data

export const useSegments = () => {
  return useQuery({
    queryKey: ['segments-summary'],
    queryFn: fetchSegments,
    staleTime: 5 * 60 * 1000,
    gcTime: 15 * 60 * 1000,
    refetchOnWindowFocus: false,
  })
}
