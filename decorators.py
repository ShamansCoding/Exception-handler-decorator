"""Module with some useful decorators."""

import inspect
import logging

from typing import Callable, Tuple, Optional, Any, Union, Type
from functools import wraps

ExceptionType = Union[Type[Exception], Tuple[Type[Exception], ...]]


class NonExistingException(Exception):
    """Stub for exception_handler."""


def exception_handler(error_message: str = 'UNSET',
                      additional_handler: Optional[Callable] = None,
                      logger_name: str = __name__,
                      exception: ExceptionType = Exception,
                      pass_exception: ExceptionType = NonExistingException,
                      pass_exception_return: Any = None,
                      additional_log_data: Optional[Callable] = None) -> Any:
    r"""Wrap error handling logic.

    Logging decorator with detailed log output.
    Can take optional handler to post processing after error.

    :param str error_message: default UNSET
    :param func additional_handler: post processing handler, called with\
    args and kwargs of decorated function
    :param str logger_name: name of the logger in settings, default __name___
    :param Exception exception: types of exceptions to handle,\
    default Exception
    :param Exception pass_exception: types of exceptions to pass, default\
    NonExistingException
    :param any pass_exception_return: return for ignored Exception
    :param func additional_log_data: func wich return some logger specific \
    info spec: (*args,**kwargs) -> str

    :return: 0 or additional_handler return
    :rtype: any
    """
    log = logging.getLogger(logger_name)

    def decorator(function: Callable):

        @wraps(function)
        def inner(*args, **kwargs):

            try:
                result = function(*args, **kwargs)
            except pass_exception:
                return pass_exception_return
            except exception as emsg:
                stack = inspect.trace()
                context_text = str(stack[-1].frame.f_locals)[:1500]
                new_line = '\n'

                trace = [(f'    [FILE: {frame.filename} => FUNC: '
                          f'{frame.function} => LINE: {frame.lineno}]\n')
                         for frame in stack]

                message = f'\n[EMSG: {error_message}]\n'

                if callable(additional_log_data):
                    message += \
                        f'[EINFO:\n    ' \
                        f'{additional_log_data(*args, **kwargs)}\n]\n'

                message += (
                    f'[STACK:\n{"".join(trace).strip(new_line)}\n]\n'
                    f'[CONTEXT:\n    {context_text}\n]\n'
                    f'[DETAIL:\n     {emsg}\n]'
                )

                log.error(message)

                if callable(additional_handler):
                    result = additional_handler(*args, **kwargs)
                    return result
                return 0
            return result
        return inner
    return decorator
