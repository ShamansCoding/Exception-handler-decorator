# Exception-handler-decorator
Useful decorator to handle exceptions with logging support and additional handlers if exception occurs. 

Examples:

```python
def handler_function(need_error, result):
    return (result, need_error)

@exception_handler(error_message='TEST',
                   additional_handler=handler_function)
def testing_func(need_error, result):
    if not need_error:
        return result

    raise Exception('test')
    
testing_func(True, 1)
```

Output:

```
[EMSG: TEST]
[STACK:
    [FILE: /home/decorators.py => FUNC: inner => LINE: 48]
    [FILE: tests.py => FUNC: testing_func => LINE: 19]
]
[CONTEXT:
    {'result': 1, 'need_error': True}
]
[DETAIL:
     test
]
```

```python
@exception_handler()
def only_err():
    raise Exception('test')

only_err()
```

Output:

```
[EMSG: UNSET]
[STACK:
    [FILE: /home/decorators.py => FUNC: inner => LINE: 48]
    [FILE: tests.py => FUNC: only_err => LINE: 31]
]
[CONTEXT:
    {}
]
[DETAIL:
     test
]
```

```python
@exception_handler(error_message='TEST',
                   additional_handler=handler_function,
                   additional_log_data=lambda ne, res: str(res))
def testing_func_one(need_error, result):
    if not need_error:
        return result

    raise Exception('test')

testing_func_one(False, 1)
```

```
[EMSG: TEST]
[EINFO:
    1
]
[STACK:
    [FILE: /home/decorators.py => FUNC: inner => LINE: 48]
    [FILE: tests.py => FUNC: testing_func_one => LINE: 44]
]
[CONTEXT:
    {'result': 1, 'need_error': True}
]
[DETAIL:
     test
]
```
