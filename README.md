#### Install

pip install hoodlogger


#### Usage

Add our decorator about the functions

@hood_thread_logger()

Will add a hood logger print to the start and end of the function

@flask_api_headers

Will read trace params from the HTTP request headers and add it to the threadLocal storage data


Code Example:

from hoodlogger.decorators import flask_api_headers, hood_thread_logger
from hoodlogger.hoodthreadlogger import HoodThreadLogger

@hood_thread_logger()
def func1(*args, **kwargs):
    logger, _ = HoodThreadLogger.get_logger(is_child=False) # -> get the current logger
    print(1)
    logger.warn('test in function') # -> add a custom warn msg to the logs
    print(2)
    print('11111111')


@hood_thread_logger(name="custom function name", new_process_name='asaf test')
def func2(*args, **kwargs):
    print('2222222')


class Link(Resource):
    # @flask_api_headers # -> read from HTTP headers and add to threadLocal storage
    @hood_thread_logger(name="link get request") # -> add hood_thread_logger() decorator 
    def get(self, *args, **kwargs):
        """Link player id with a user"""
        print(2222222)

        # time.sleep(3)
        func1()
        func2()
        func2()
        return {'status': 'linked with %s from %s' % ("1", "2")}

