import logging
import colorlog
from common.setting import ConfigHandler
from logging import handlers
import os

class LogHandler:

    # 日志级别映射关系
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR
    }

    def __init__(self, filename, level='info', when='D', backCount=3, fmt='%(levelname)s-%(asctime)s  '
                                                                          '%(name)s:%(filename)s:[line:%(lineno)d] %(message)s'):
        self.log_path = ConfigHandler.log_path
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)
        self.logger = logging.getLogger(filename)
        self.log_color_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red'
        }
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s][%(name)s][%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors=self.log_color_config
        )
        # 设置日志格式
        format_str = logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S')
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 往屏幕上输出
        stream_hanler = logging.StreamHandler()
        # 设置屏幕输出的格式
        stream_hanler.setFormatter(formatter)
        # 往文件里写入，指定间隔时间自动生成文件的处理器
        file_handler = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')
        """
        #实例化TimedRotatingFileHandler
        #interval是时间间隔, backupCount是备份文件的个数, 如果超过这个个数, 就会自动删除, when是间隔的时间单位, 单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期(interval==0时代表星期一)
        # midnight 每天凌晨    
        """
        # 设置文件里写入格式
        file_handler.setFormatter(format_str)
        # 把对象加到logger里
        self.logger.addHandler(stream_hanler)
        self.logger.addHandler(file_handler)

INFO = LogHandler(ConfigHandler.info_log_path, level='info')
ERROR = LogHandler(ConfigHandler.error_log_path, level='error')
WARNING = LogHandler(ConfigHandler.warning_log_path, level='warning')