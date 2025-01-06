__all__ = [
    'log_full',
    'log_stack',
    'log_timer',
    'log_exceptions',
    'with_info',
    'with_return'
]

import functools
import time

from .strings import decorating, str_type


# bread is very delicious
def bread(
        begin=None,
        end=None,
        exp=None
):
    def decorator(f):

        @functools.wraps(f)
        def wrapper(*args, **kwargs):

            if begin is not None:
                message = begin(f, *args, **kwargs)
            else:
                message = None

            ret = None
            try:
                ret = f(*args, **kwargs)
            except Exception as e:
                handled = False
                if exp is not None:
                    handled = exp(e)
                if not handled:
                    raise e

            if end is not None:
                if message is not None:
                    kwargs['message_by_begin'] = message
                if ret is not None:
                    kwargs['message_by_function'] = ret

                end(f, *args, **kwargs)

            return ret

        return wrapper

    return decorator


def log_enter(
        handler,
        logArgs: bool = False
):
    def log_debug(f, *args, **kwargs):
        if logArgs:
            arg = "(" + ", ".join([repr(x) for x in args] + [f"{k}={v!r}" for k, v in kwargs.items()]) + ")"
            message = f"Calling {decorating(f.__name__, 32)}{arg}"
        else:
            message = f"+ {decorating(f.__name__, 32)}"

        handler(message)

    return log_debug


def add_logging(f):
    """A type-safe decorator to add logging to a function."""

    def inner(*args, **kwargs):
        return f(*args, **kwargs)

    return inner


def log_exit(
        handler,
        logRets: bool = False
):
    def log_debug(f, *args, **kwargs):
        if logRets:
            ret = " returned " + repr(kwargs['message_by_function'])
            message = f"{decorating(f.__name__, 31)}{ret}"
        else:
            message = f"- {decorating(f.__name__, 31)}"

        handler(message)

    return log_debug


def log_full(
        handler
):
    return bread(log_enter(handler, True), log_exit(handler, True))


def log_stack(
        handler
):
    return bread(log_enter(handler), log_exit(handler))


def log_timer(
        handler
):
    def begin(*args, **kwargs):
        return time.perf_counter()

    def end(*args, **kwargs):
        message = f"for {decorating(time.perf_counter() - kwargs['message_by_begin'], 32)}s"
        handler(message)

    return bread(begin, end)


def log_exceptions(
        handler
):
    def log_error(e):
        message = decorating(f"{str_type(e)} : {e}", 31)
        handler(message)

    return bread(exp=log_error)


def with_info(
        handler,
        begin=None,
        end=None,
        report_params=False
):
    def info_begin(f, *args, **kwargs):
        if begin is not None:
            if report_params:
                handler(begin, *args, **kwargs)
            else:
                handler(begin)

    def info_end(f, *args, **kwargs):
        if end is not None:
            if report_params:
                handler(end, *args, **kwargs)
            else:
                handler(end)

    return bread(info_begin, info_end)


def with_return(
        _type
):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs) -> _type:
            ret = f(*args, **kwargs)
            if isinstance(ret, _type):
                return ret
            else:
                return _type(ret)

        return wrapper

    return decorator
