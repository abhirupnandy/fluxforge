export type TaskType = 'DOWNLOAD' | 'ENCODE'
export type TaskState = 'PENDING' | 'QUEUED' | 'STARTING' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'CANCELLING' | 'CANCELLED'
export interface Task { id:string; task_type:TaskType; state:TaskState; progress:number; payload:Record<string,unknown>; logs?:string|null; retry_count:number; error_message?:string|null; created_at:string; updated_at:string; started_at?:string|null; completed_at?:string|null }
export interface TaskCreateInput { payload: Record<string, unknown> }
export interface TaskEvent { event:'task.created'|'task.queued'|'task.started'|'task.progress'|'task.completed'|'task.failed'|'task.cancelled'|'task.log'; task_id:string; timestamp:string; data:Record<string,unknown> }
