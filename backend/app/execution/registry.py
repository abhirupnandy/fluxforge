from app.execution.workers.ffmpeg_worker import FFmpegWorker
from app.execution.workers.yt_dlp_worker import YtDlpWorker
WORKERS={'DOWNLOAD':YtDlpWorker,'ENCODE':FFmpegWorker}
