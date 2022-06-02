import os

class ConfigHandler:
    _SLASH = os.sep

    # 项目路径
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 用例路径
    case_path = os.path.join(root_path, 'test_case' + _SLASH)

    # 测试用例数据路径
    data_path = os.path.join(root_path, 'test_data' + _SLASH)

    cache_path = os.path.join(root_path, 'cache' + _SLASH)
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)

    config_path = os.path.join(root_path, 'common' + _SLASH + 'config.yaml')

    file_path = os.path.join(root_path, 'files' + _SLASH)

    log_path = os.path.join(root_path, 'logs' + _SLASH + 'log.log')

    info_log_path = os.path.join(root_path, 'logs' + _SLASH + 'info.log')

    error_log_path = os.path.join(root_path, 'logs' + _SLASH + 'error.log')

    warning_log_path = os.path.join(root_path, 'logs' + _SLASH + 'warning.log')
    
    util_path = os.path.join(root_path, 'utils' + _SLASH)
    util_install_path = util_path + 'otherUtils' + _SLASH + 'InstallUtils' + _SLASH

    # 测试报告路径
    report_path = os.path.join(root_path, 'report')
    
    # 测试报告html路径
    report_html_path= os.path.join(root_path, 'report' + _SLASH + 'html' + _SLASH)

    # 测试报告中的test_case路径
    report_html_test_case_path = os.path.join(root_path, 'report' + _SLASH +
                                              "html" + _SLASH + 'data' + _SLASH + "test-cases" + _SLASH)

    # 测试报告中的attachments路径
    report_html_attachments_path = os.path.join(root_path, 'report' + _SLASH +
                                                "html" + _SLASH + 'data' + _SLASH + "attachments" + _SLASH)

    # 测试报告ZIP路径
    report_zip_path = os.path.join(root_path, 'utils' + _SLASH + 'noticUtils' + _SLASH)

    excel_template = os.path.join(root_path, 'utils' + _SLASH + 'otherUtils' + _SLASH + "allureDate" + _SLASH)