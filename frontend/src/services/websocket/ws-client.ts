import { env } from '../../lib/env'
import type { TaskEvent } from '../../features/tasks/types/task-types'
import { applyTaskEvent } from '../../features/tasks/reducers/task-event-reducer'
import { useWebsocketStore } from '../../stores/websocket-store'
class WsClient{ private ws:WebSocket|null=null; private timer:number|undefined; private retry=0;
connect(){if(this.ws&&(this.ws.readyState===WebSocket.OPEN||this.ws.readyState===WebSocket.CONNECTING)) return; useWebsocketStore.getState().setStatus(this.retry>0?'reconnecting':'connecting'); const url=env.VITE_API_URL.replace('http','ws')+'/ws'; this.ws=new WebSocket(url); this.ws.onopen=()=>{this.retry=0;useWebsocketStore.getState().setRetries(0);useWebsocketStore.getState().setStatus('connected')}; this.ws.onmessage=(m)=>applyTaskEvent(JSON.parse(m.data) as TaskEvent); this.ws.onclose=()=>{useWebsocketStore.getState().setStatus('disconnected'); this.scheduleReconnect()}}
private scheduleReconnect(){this.retry+=1; useWebsocketStore.getState().setRetries(this.retry); this.timer=window.setTimeout(()=>this.connect(),Math.min(10000,500*this.retry))}
disconnect(){if(this.timer) clearTimeout(this.timer); this.ws?.close(); this.ws=null; useWebsocketStore.getState().setStatus('disconnected')}}
export const wsClient=new WsClient()
