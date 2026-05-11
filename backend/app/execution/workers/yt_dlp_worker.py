from app.execution.base_worker import BaseWorker
from app.execution.progress.yt_dlp_parser import parse_yt_dlp_line
from app.queue import task_events
class YtDlpWorker(BaseWorker):
 async def execute(self,task):
  async def on_line(src,line):
   await self.repo.append_log(task,f'[{src}] {line}'); await self.broadcaster.emit(task_events.TASK_LOG,task.id,{'line':line})
   p=parse_yt_dlp_line(line)
   if p and p.percentage is not None: await self.repo.update_progress(task,p.percentage); await self.broadcaster.emit(task_events.TASK_PROGRESS,task.id,p.model_dump())
  return await self.runner.run(task.payload.get('command',['yt-dlp',task.payload.get('url','')]),on_line,self.cancel_event)
