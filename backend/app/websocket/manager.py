from fastapi import WebSocket
class WebsocketManager:
    def __init__(self): self.connections:set[WebSocket]=set()
    async def connect(self,ws:WebSocket)->None: await ws.accept(); self.connections.add(ws)
    def disconnect(self,ws:WebSocket)->None: self.connections.discard(ws)
    async def broadcast(self,payload:dict)->None:
        dead=[]
        for c in self.connections:
            try: await c.send_json(payload)
            except Exception: dead.append(c)
        for c in dead: self.disconnect(c)
