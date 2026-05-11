import re
from app.schemas.execution import ProgressEvent
PERCENT_RE=re.compile(r'(\d+(?:\.\d+)?)%'); ETA_RE=re.compile(r'ETA\s+(\S+)'); SPEED_RE=re.compile(r'at\s+(\S+/s)')
def parse_yt_dlp_line(line:str)->ProgressEvent|None:
    if '[download]' not in line: return None
    p=PERCENT_RE.search(line)
    return ProgressEvent(percentage=float(p.group(1)) if p else None, eta=(ETA_RE.search(line).group(1) if ETA_RE.search(line) else None), speed=(SPEED_RE.search(line).group(1) if SPEED_RE.search(line) else None))
