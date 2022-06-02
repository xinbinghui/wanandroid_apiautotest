from utils.readfilesUtils.yamlControl import GetYamlData
from common.setting import ConfigHandler

conf = GetYamlData(ConfigHandler.config_path).get_yaml_data()

def sql_switch():
    """获取数据库开关"""
    switch = conf['MySqlDB']['switch']
    return switch

def get_notification_type():
    # 获取报告通知类型
    return conf['NotificationType']

def get_mirror_url():
    """获取镜像源"""
    mirror_url = conf['mirror_source']
    return mirror_url

project_name = conf['ProjectName'][0]