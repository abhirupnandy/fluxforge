import { api } from '../../lib/api/client'
import type { Task, TaskCreateInput } from '../../features/tasks/types/task-types'
export const tasksApi={createDownload:async(i:TaskCreateInput)=>(await api.post<Task>('/tasks/download',i)).data,createEncode:async(i:TaskCreateInput)=>(await api.post<Task>('/tasks/encode',i)).data,list:async()=>(await api.get<Task[]>('/tasks')).data,cancel:async(id:string)=>(await api.post<Task>(`/tasks/${id}/cancel`)).data}
