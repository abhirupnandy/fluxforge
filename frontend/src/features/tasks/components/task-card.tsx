import type { Task } from '../types/task-types'

export function TaskCard({ task, onCancel, onSelect }: { task: Task; onCancel?: (id: string) => void; onSelect?: (id: string) => void }) {
  return <div className='rounded border border-slate-700 p-3 text-sm'><div className='flex items-center justify-between'><button onClick={()=>onSelect?.(task.id)} className='font-semibold'>{task.task_type} · {task.id.slice(0,8)}</button><span>{task.state}</span></div><div className='mt-2 h-2 w-full rounded bg-slate-800'><div className='h-2 rounded bg-cyan-500' style={{width:`${task.progress ?? 0}%`}}/></div>{onCancel && <button className='mt-2 rounded bg-rose-600 px-2 py-1' onClick={()=>onCancel(task.id)}>Cancel</button>}</div>
}
