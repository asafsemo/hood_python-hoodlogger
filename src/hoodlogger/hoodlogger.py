import json
import os
import datetime
import copy
import random
import sys
import numpy as np

_levels = {
    "verbose": 10,
    "debug": 20,
    "info": 30,
    "warn": 40,
    "error": 50,
    "fatal": 60,
    10: 'verbose',
    20: 'debug',
    30: 'info',
    40: 'warn',
    50: 'error',
    60: 'fatal',
}


class HoodLogger:
    def __init__(self, name: str, min_level: str = 'info', is_root: bool = True, trace_id: any = None, parent_id: any = None, current_id: any = None, *args, **kwargs):
        self._log_stream = print
        # self._log_stream = sys.stdout.write
        self._min_level = min_level
        self._is_root = is_root
        self._disable_trace_logging = kwargs.get(
            'disable_trace_logging', False)
        self._default_log = {
            "name": str(name),
            "pid": os.getpid(),
            "hostname": kwargs.get('hostname', "NONE"),
            "v": kwargs.get('v', "0")
        }
        random_int64 = np.random.randint(1, 9223372036854775807, 2)
        self._trace = {
            "id": str(trace_id or random_int64[0]),
            "current": str(current_id or random_int64[1]),
        }
        if (parent_id is not None):
            self._trace['parent'] = str(parent_id)

    def create_child_trace_logger(self, name: any = None, min_level: any = None, **kwargs):
        child_level = min_level or self._min_level
        child_name = name or self._default_log['name'] + '-child'
        # let { minLevel, trace, ...restOptions } = options || {};
        # let {current, ...restTrace} = this._trace
        # restOptions.trace = Object.assign({}, restTrace, trace)
        # let newOptions = Object.assign({}, this._options, restOptions)
        return HoodLogger(name=child_name, min_level=child_level, is_root=False,
                          trace_id=self._trace['id'], parent_id=self._trace['current'], **kwargs)

    def get_trace_context(self):
        pass

    def info(self, msg, trace: dict = None, tags: dict = None, *args, **kwargs):
        return self._write_log_with_level(msg, _levels['info'], self._log_stream,
                                          trace=trace, tags=tags,
                                          *args, **kwargs)

    def warn(self, msg, trace: dict = None, tags: dict = None, *args, **kwargs):
        return self._write_log_with_level(msg, _levels['warn'], self._log_stream,
                                          trace=trace, tags=tags,
                                          *args, **kwargs)

    def end(self, msg, trace: dict = None, tags: dict = None, *args, **kwargs):
        trace = trace or {}
        trace['status'] = 'complete' if self._is_root else 'end'
        self._write_log(msg, _levels['info'], self._log_stream,
                        trace=trace, tags=tags,
                        *args, **kwargs)
        sys.stdout.flush()

    def _write_log_with_level(self, msg, level, stream, trace: dict, tags: dict, *args, **kwargs):
        if (level < _levels[self._min_level]):
            return

        return self._write_log(msg, level, stream,
                               trace=trace, tags=tags,
                               *args, **kwargs)

    def _write_log(self, msg, level, stream, trace: dict, tags: dict, *args, **kwargs):
        current_log = copy.deepcopy(self._default_log)
        current_log['time'] = datetime.datetime.utcnow(
        ).isoformat(timespec='milliseconds') + 'Z'
        current_log['level'] = level
        current_log['lvl_name'] = _levels[level]
        current_log['msg'] = msg

        # restOptions
        for key, value in kwargs.items():
            current_log[key] = value

        trace_obj = self._build_trace_object(trace, tags)
        if (trace_obj is not None):
            current_log['trace'] = trace_obj

        stream(json.dumps(current_log))

    def _build_trace_object(self, trace, tags):
        if (self._disable_trace_logging):
            return None

        t_obj = copy.deepcopy(self._trace)
        if (trace is not None):
            for key, value in trace.items():
                t_obj[key] = value

    #     let tTags = tags or t.tags

    #     if (not Object.keys(t).length and not tTags) {
    #         return null
    #     }

    #     if (not logger._trace or not logger._trace.id) {
    #         return null
    #     }

    #     if (tTags) {
    #         t.tags = tTags
    #     }
        return t_obj
