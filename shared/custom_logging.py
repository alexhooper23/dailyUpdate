from datetime import datetime
import os
import inspect
from inspect import currentframe


# This class is defined to ensure the correct file path when this file is called from somewhere else.
class Dummy:
    print()


def validate_bool(check_itm, kind="This variable"):
    if isinstance(check_itm, bool):
        return check_itm
    else:
        raise TypeError(f"{kind} must be a Boolean value.")


class Log:
    """
    This class defines logging rules for both console and text file logging.
    :param file_enable_state: True
    :param console_enable_state: False
    """
    combined_logging = True
    log_folder = os.path.dirname(os.path.dirname(inspect.getfile(Dummy))) + "/data/private/logs/"

    def __init__(self, file_enable_state=True, console_enable_state=True):
        self.console_enable = validate_bool(console_enable_state, "Console logging state")
        self.file_enable = validate_bool(file_enable_state, "File logging state")
        running_file_name = currentframe().f_back.f_code.co_filename.split('/')[-1]
        print("Logging from: " + running_file_name)
        self.log_file_name = f"{self.log_folder}{running_file_name[0:-3]}.log"
        print("Logging file: " + self.log_file_name)
        with open(self.log_file_name, "a") as log_file:
            print("Executing default track.......")
            log_file.write(f"\n--> {str(datetime.now())} New session created.\n")
            log_file.close()
        if self.__class__.combined_logging:
            with open(f"{self.log_folder}/_combined.log", "a") as log_file:
                log_file.write(f"\n--> {str(datetime.now())} New session created for {running_file_name}\n")
                log_file.close()

    def console_logs(self, console_logging):
        """
        Enable or disable logging to the console with a Boolean value.
        :param console_logging:
        :return:
        """
        self.console_enable = validate_bool(console_logging, "Console logging state")

    def file_logs(self, file_logging):
        """
        Enable or disable logging to a log file with a Boolean value.
        :param file_logging:
        :return:
        """
        self.file_enable = validate_bool(file_logging, "File logging state")

    def log(self, text="session_start"):
        """
        Writes item to log.
        :param text:
        :return:
        """
        text = str(text)
        if self.console_enable:
            print(text)
        if self.file_enable:
            log_output = f"{str(datetime.now())}\t{text}\n"
            with open(self.log_file_name, "a") as log_file:
                log_file.write(log_output)
                log_file.close()
            if self.__class__.combined_logging:
                with open(f"{self.log_folder}/_combined.log", "a") as log_file:
                    log_file.write(log_output)
                    log_file.close()

    def clear_log(self):
        """
        Clears log for current object
        :return:
        """
        open(self.log_file_name, "w").close()

    @staticmethod
    def clear_logs():
        """
        Clears all logs in the logs directory.
        :return:
        """
        for filename in os.listdir("data/private/logs/"):
            open(filename, "w").close()
