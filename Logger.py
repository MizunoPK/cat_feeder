from Config import Config
import datetime

# Class: Logger
# Description: Manages logging info to the console
class Logger:
    @staticmethod
    def log(type, level, message):
        if level <= Config.LOG_LEVELS[type]:
            time = datetime.datetime.now().time()
            print(f'<{time}> {type.value} --- {message}')