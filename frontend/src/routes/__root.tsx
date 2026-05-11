import { createRootRoute } from '@tanstack/react-router'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

import { Toaster } from 'sonner'

import { AppShell } from '../components/layout/app-shell'

import { ErrorBoundary } from '../components/layout/error-boundary'

const queryClient = new QueryClient()

export const Route = createRootRoute({
  component: RootComponent,
})

function RootComponent() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <AppShell />

        <Toaster richColors position="top-right" />
      </QueryClientProvider>
    </ErrorBoundary>
  )
}
