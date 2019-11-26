import functools

from flask import request
from .hoodthreadlogger import HoodThreadLogger


__all__ = ['flask_api_headers', 'hood_thread_logger']


def flask_api_headers(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        trace_id = request.headers.get('x-cloud-trace-context')
        if trace_id:
            trace_id = trace_id.split('/')[0]
        parent_id = request.headers.get('x-trace-parent-id')

        HoodThreadLogger.set_hood_data(trace_id, parent_id)
        return func(*args, **kwargs)
    return wrapper


def hood_thread_logger(name: str = None, new_process_name: str = None, is_child: bool = True, disable_trace_logging: bool = False):
    def decorator(func):
        """Print the function signature and return value"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger, is_end = HoodThreadLogger.get_logger(
                name=(name or func.__name__), is_child=is_child, disable_trace_logging=disable_trace_logging, **kwargs)

            if (logger is None):
                return func(*args, **kwargs)

            trace_obj = None
            if (new_process_name is not None):
                trace_obj = {'type': new_process_name}

            logger.info('start message', trace=trace_obj)

            result = func(*args, **kwargs)

            if is_end:
                logger.end('end message')
            return result
        return wrapper
    return decorator
