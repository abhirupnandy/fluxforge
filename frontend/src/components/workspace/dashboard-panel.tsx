import { useHealth } from '../../hooks/use-health'

export function DashboardPanel() {
  const { data, isLoading, isError } = useHealth()

  let status = 'checking...'

  if (isLoading) {
    status = 'checking...'
  } else if (isError) {
    status = 'backend offline'
  } else if (data) {
    status = data.status
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-5xl font-bold">FluxForge</h1>

        <p className="mt-2 text-slate-400">Media processing platform</p>
      </div>

      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <h2 className="mb-2 text-xl font-semibold">Backend Status</h2>

        <p className="text-lg">{status}</p>
      </div>
    </div>
  )
}
