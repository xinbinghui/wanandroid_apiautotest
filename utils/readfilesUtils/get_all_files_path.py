import os

def get_all_files(file_path, yaml_data_switch=False):
    """
    获取文件路径
    :param file_path:
    :param yaml_data_switch: 是否过滤文件为 yaml格式, True则过滤
    :return:
    """
    filename=[]
    for root, dirs, files in os.walk(file_path):
        for filepath in files:
            path = os.path.join(root, filepath)
            if yaml_data_switch:
                if 'yaml' in path or 'yml' in path:
                    filename.append(path)
            else:
                filename.append(path)
    return filename