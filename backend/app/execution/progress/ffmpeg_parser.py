import re
from app.schemas.execution import ProgressEvent
TIME_RE=re.compile(r'time=(\d+):(\d+):(\d+\.\d+)'); FPS_RE=re.compile(r'fps=\s*(\S+)'); BIT_RE=re.compile(r'bitrate=\s*(\S+)')
def parse_ffmpeg_line(line:str,duration_seconds:float|None=None)->ProgressEvent|None:
 m=TIME_RE.search(line)
 if not m:return None
 t=int(m.group(1))*3600+int(m.group(2))*60+float(m.group(3)); pct=(t/duration_seconds*100.0) if duration_seconds else None; fps=FPS_RE.search(line); br=BIT_RE.search(line)
 return ProgressEvent(percentage=pct,fps=float(fps.group(1)) if fps and fps.group(1).replace('.','',1).isdigit() else None,bitrate=br.group(1) if br else None)
