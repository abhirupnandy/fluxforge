import { useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { tasksApi } from '../../../services/api/tasks-api'
import { useTaskStore } from '../../../stores/task-store'
import { wsClient } from '../../../services/websocket/ws-client'

export function useTaskSync(){
  const upsert=useTaskStore((s)=>s.upsertTask)
  useQuery({queryKey:['tasks'], queryFn: tasksApi.list, refetchOnWindowFocus:false, retry:1})
  const { data } = useQuery({queryKey:['tasks-bootstrap'], queryFn: tasksApi.list})
  useEffect(()=>{data?.forEach(upsert)},[data,upsert])
  useEffect(()=>{wsClient.connect(); return ()=>wsClient.disconnect()},[])
}
