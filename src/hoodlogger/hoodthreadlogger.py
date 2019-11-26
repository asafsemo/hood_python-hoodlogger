import threading

from .hoodlogger import HoodLogger

threadLocal = threading.local()


class HoodThreadLogger(HoodLogger):
    _activate=True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        threadLocal.loggers.insert(0, self)

    @classmethod
    def set_hood_data(cls, trace_id, parent_id=None, current_id=None):
        threadLocal.trace_id = trace_id
        threadLocal.parent_id = parent_id
        threadLocal.current_id = current_id

    @classmethod
    def config(cls, activate = True, *args, **kwargs):
        cls._activate = activate

    @classmethod
    def get_logger(cls, name=None, is_child=True, default_logger = None, **kwargs):
        if (not cls._activate):
            return default_logger, False

        loggers = getattr(threadLocal, 'loggers', None)
        if (loggers is None):
            threadLocal.loggers = []
            # this is root
            root_logger = HoodThreadLogger(
                name=name,
                trace_id=getattr(threadLocal, 'trace_id', None),
                parent_id=getattr(threadLocal, 'parent_id', None), **kwargs)

            # threadLocal.loggers.insert(0, root_logger)
            return root_logger, True

        if (not is_child):
            return threadLocal.loggers[0], False

        logger = threadLocal.loggers[0].create_child_trace_logger(
            name, **kwargs)
        return logger, True

    def create_child_trace_logger(self, name: any = None, min_level: any = None, **kwargs):
        child_level = min_level or self._min_level
        child_name = name or self._default_log['name'] + '-child'
        return HoodThreadLogger(name=child_name, min_level=child_level, is_root=False,
                                trace_id=self._trace['id'], parent_id=self._trace['current'],
                                **kwargs)

    def end(self, *args, **kwargs):
        super().end(*args, **kwargs)
        return threadLocal.loggers.pop(0)
