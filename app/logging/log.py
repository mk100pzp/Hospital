import logging

logging.basicConfig(filename='D:\SRC\Python\GW1\week_13\app\logging\log_info.txt', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Define a decorator function
def log_function_call(func):
    def wrapper(*args, **kwargs):
        # Log the function call with its name, arguments, and the start time
        function_name = func.__name__
        logging.info(f"Calling {function_name} with args={args} and kwargs={kwargs}")

        try:
            # Execute the wrapped function
            result = func(*args, **kwargs)

            # Log the return value
            logging.info(f"{function_name} returned {result}")
            return result
        except Exception as e:
            # Log any exceptions that occur
            logging.error(f"Exception in {function_name}: {e}")
            raise

    return wrapper

# Apply the decorator to a function
#@log_function_call

