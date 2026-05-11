import { create } from 'zustand'
export const useQueueStore=create<{selectedTaskId:string|null;setSelectedTaskId:(id:string|null)=>void}>((set)=>({selectedTaskId:null,setSelectedTaskId:(selectedTaskId)=>set({selectedTaskId})}))
