import { useMutation } from '@tanstack/react-query'
import { tasksApi } from '../../services/api/tasks-api'
import { useTaskStore } from '../../stores/task-store'
import { useQueueStore } from '../../stores/queue-store'
import { TaskCard } from '../../features/tasks/components/task-card'

export function EncoderPanel() {
  const grouped = useTaskStore((s) => s.grouped())
  const upsert = useTaskStore((s) => s.upsertTask)
  const setSelected = useQueueStore((s) => s.setSelectedTaskId)
  const create = useMutation({ mutationFn: tasksApi.createEncode, onSuccess: upsert })
  const cancel = useMutation({ mutationFn: tasksApi.cancel, onSuccess: upsert })
  return <div className='space-y-4'><button className='rounded bg-violet-600 px-3 py-2' onClick={()=>create.mutate({payload:{command:['ffmpeg','-version']}})}>New Encode</button><div className='space-y-2'>{[...grouped.queued,...grouped.running].filter(t=>t.task_type==='ENCODE').map((t)=><TaskCard key={t.id} task={t} onCancel={(id)=>cancel.mutate(id)} onSelect={setSelected} />)}</div></div>
}
