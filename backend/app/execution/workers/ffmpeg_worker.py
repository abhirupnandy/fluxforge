from app.execution.base_worker import BaseWorker
from app.execution.progress.ffmpeg_parser import parse_ffmpeg_line
from app.queue import task_events
class FFmpegWorker(BaseWorker):
 async def execute(self,task):
  duration=task.payload.get('duration_seconds')
  async def on_line(src,line):
   await self.repo.append_log(task,f'[{src}] {line}'); await self.broadcaster.emit(task_events.TASK_LOG,task.id,{'line':line})
   p=parse_ffmpeg_line(line,duration)
   if p and p.percentage is not None: await self.repo.update_progress(task,p.percentage); await self.broadcaster.emit(task_events.TASK_PROGRESS,task.id,p.model_dump())
  return await self.runner.run(task.payload.get('command',['ffmpeg']),on_line,self.cancel_event)
