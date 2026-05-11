from collections.abc import Mapping
from app.schemas.task import TaskState
ALLOWED_TRANSITIONS: Mapping[TaskState,set[TaskState]]={TaskState.PENDING:{TaskState.QUEUED,TaskState.CANCELLED},TaskState.QUEUED:{TaskState.STARTING,TaskState.CANCELLING,TaskState.CANCELLED},TaskState.STARTING:{TaskState.RUNNING,TaskState.FAILED,TaskState.CANCELLING},TaskState.RUNNING:{TaskState.COMPLETED,TaskState.FAILED,TaskState.CANCELLING},TaskState.CANCELLING:{TaskState.CANCELLED,TaskState.FAILED},TaskState.COMPLETED:set(),TaskState.FAILED:set(),TaskState.CANCELLED:set()}
class InvalidStateTransition(ValueError): pass
def ensure_transition(current:TaskState,new:TaskState)->None:
 if new not in ALLOWED_TRANSITIONS[current]: raise InvalidStateTransition(f'Invalid transition {current}->{new}')
