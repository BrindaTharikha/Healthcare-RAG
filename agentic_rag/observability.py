import contextvars
import json
import time
import uuid
from contextlib import contextmanager

from . import config

_log_dir = config.log_dir

# The "sticky note" — holds the currently active trace_id so log_event()
# can find it automatically without you passing trace_id= every time.
_current_trace_id = contextvars.ContextVar("trace_id", default="")


def new_trace_id() -> str:
    random_id = uuid.uuid4()
    id_as_text = str(random_id)
    short_id = id_as_text[0:12]
    return short_id


def log_event(event, trace_id=None, **extra_fields):
    record = {
        "event": event,
        "trace_id": trace_id or _current_trace_id.get(""),
        "timestamp": time.time(),
        **extra_fields,
    }
    with open(_log_dir / "events.jsonl", "a") as f:
        f.write(json.dumps(record, default=str) + "\n")


@contextmanager
def trace(trace_id: str | None = None):
    tid = trace_id or new_trace_id()
    token = _current_trace_id.set(tid)
    log_event("trace_start", trace_id=tid)
    try:
        yield tid
    finally:
        log_event("trace_end", trace_id=tid)
        _current_trace_id.reset(token)


@contextmanager
def timed(step: str, **fields):
    start = time.perf_counter()
    error = None
    try:
        yield
    except Exception as e:
        error = repr(e)
        raise
    finally:
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        log_event("step", step=step, duration_ms=duration_ms, error=error, **fields)


def read_events(trace_id: str | None = None) -> list[dict]:
    path = _log_dir / "events.jsonl"
    if not path.exists():
        return []
    results = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if trace_id is None or record.get("trace_id") == trace_id:
                results.append(record)
    return results