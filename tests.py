import unittest
import logging

from unittest.mock import patch

from decorators import exception_handler

logging.disable(logging.CRITICAL)

class ExceptionHandlerTests(unittest.TestCase):

    def test_exception_handler(self):

        def handler_function(need_error, result):
            return (result, need_error)

        @exception_handler(error_message='TEST',
                           additional_handler=handler_function)
        def testing_func(need_error, result):
            if not need_error:
                return result

            raise Exception('test')

        result = testing_func(False, 1)

        self.assertEqual(result, 1)

        handler_result = testing_func(True, 1)

        self.assertEqual(handler_result, (1, True))

        @exception_handler()
        def only_err():
            raise Exception('test')

        result = only_err()

        self.assertEqual(result, 0)

        @exception_handler(error_message='TEST',
                           additional_handler=handler_function,
                           additional_log_data=lambda ne, res: str(res))
        def testing_func_one(need_error, result):
            if not need_error:
                return result

            raise Exception('test')

        result = testing_func_one(False, 1)

        self.assertEqual(result, 1)

        handler_result = testing_func_one(True, 1)

        self.assertEqual(handler_result, (1, True))

if __name__ == '__main__':

    unittest.main()
