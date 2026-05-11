import { useTaskStore } from '../../stores/task-store'
import { useQueueStore } from '../../stores/queue-store'

export function QueuePanel() {
  const grouped = useTaskStore((s) => s.grouped())
  const selectedId = useQueueStore((s) => s.selectedTaskId)
  const selected = useTaskStore((s) => (selectedId ? s.tasksById[selectedId] : null))
  return <div className='grid grid-cols-2 gap-4'><div><h3>Queued</h3>{grouped.queued.map((t)=><div key={t.id}>{t.id.slice(0,8)} {t.state} {Math.round(t.progress)}%</div>)}<h3 className='mt-4'>Running</h3>{grouped.running.map((t)=><div key={t.id}>{t.id.slice(0,8)} {t.state}</div>)}<h3 className='mt-4'>Completed</h3>{grouped.completed.map((t)=><div key={t.id}>{t.id.slice(0,8)} {t.state}</div>)}</div><div><h3>Task Logs</h3><pre className='h-[420px] overflow-auto rounded bg-slate-900 p-3 text-xs'>{selected?.logs || 'Select a task from Downloads/Encoder panels.'}</pre></div></div>
}
