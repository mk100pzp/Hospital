import logging

logging.basicConfig(filename='D:\SRC\Python\GW1\week_13\app\logging\log_info.txt', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode='w')


def log_function_call(func):
    def wrapper(*args, **kwargs):
        function_name = func.__name__
        logging.info(f"Calling {function_name} with args={args} and kwargs={kwargs}")

        try:

            result = func(*args, **kwargs)

            logging.info(f"{function_name} returned {result}")
            return result
        except Exception as e:

            logging.error(f"Exception in {function_name}: {e}")
            raise

    return wrapper

# Apply the decorator to a function
# @log_function_call
