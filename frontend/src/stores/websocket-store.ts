import { create } from 'zustand'
export type WsStatus='idle'|'connecting'|'connected'|'disconnected'|'reconnecting'
export const useWebsocketStore=create<{status:WsStatus;retries:number;setStatus:(s:WsStatus)=>void;setRetries:(r:number)=>void}>((set)=>({status:'idle',retries:0,setStatus:(status)=>set({status}),setRetries:(retries)=>set({retries})}))
