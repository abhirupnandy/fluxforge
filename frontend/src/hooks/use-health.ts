import { useQuery } from '@tanstack/react-query'

import { api } from '../lib/api/client'

import type { HealthResponse } from '../types/api'

export function useHealth() {
  return useQuery({
    queryKey: ['health'],

    queryFn: async () => {
      const response = await api.get<HealthResponse>('/health')

      return response.data
    },

    refetchInterval: 10000,
  })
}
