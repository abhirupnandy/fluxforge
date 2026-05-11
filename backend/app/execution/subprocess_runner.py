import asyncio, contextlib, signal
from collections.abc import Awaitable, Callable
from app.schemas.execution import ExecutionResult
class SubprocessRunner:
    async def run(self,cmd:list[str],on_line:Callable[[str,str],Awaitable[None]],cancel_event:asyncio.Event,timeout:float|None=None)->ExecutionResult:
        proc=await asyncio.create_subprocess_exec(*cmd,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
        logs=[]
        async def rd(pipe,src):
            while True:
                b=await pipe.readline()
                if not b: break
                t=b.decode(errors='ignore').rstrip(); logs.append(f'[{src}] {t}'); await on_line(src,t)
        streams=[asyncio.create_task(rd(proc.stdout,'stdout')),asyncio.create_task(rd(proc.stderr,'stderr'))]
        while proc.returncode is None:
            if cancel_event.is_set():
                with contextlib.suppress(ProcessLookupError): proc.send_signal(signal.SIGTERM)
                break
            await asyncio.sleep(0.2)
        await asyncio.wait_for(proc.wait(), timeout=timeout)
        await asyncio.gather(*streams, return_exceptions=True)
        return ExecutionResult(returncode=proc.returncode or 0, logs=logs)
