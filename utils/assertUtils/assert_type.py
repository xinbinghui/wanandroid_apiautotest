builtin_str = str
integer_types = int


def equals(check_value, expect_value):
    """判断是否相等"""

    assert check_value == expect_value


def less_than(check_value, expect_value):
    """判断实际结果小于预期结果"""
    assert check_value < expect_value


def less_than_or_equals(check_value, expect_value):
    """判断实际结果小于等于预期结果"""
    assert check_value <= expect_value


def greater_than(check_value, expect_value):
    """判断实际结果大于预期结果"""
    assert check_value > expect_value


def greater_than_or_equals(check_value, expect_value):
    """判断实际结果大于等于预期结果"""
    assert check_value >= expect_value


def not_equals(check_value, expect_value):
    """判断实际结果不等于预期结果"""
    assert check_value != expect_value


def string_equals(check_value, expect_value):
    """判断字符串是否相等"""
    assert builtin_str(check_value) == builtin_str(expect_value)


def length_equals(check_value, expect_value):
    """判断长度是否相等"""
    assert isinstance(expect_value, integer_types)
    assert len(check_value) == expect_value


def length_greater_than(check_value, expect_value):
    """判断长度大于"""
    assert isinstance(expect_value, integer_types)
    assert len(check_value) > expect_value


def length_greater_than_or_equals(check_value, expect_value):
    """判断长度大于等于"""
    assert isinstance(expect_value, integer_types)
    assert len(check_value) >= expect_value


def length_less_than(check_value, expect_value):
    """判断长度小于"""
    assert isinstance(expect_value, integer_types)
    assert len(check_value) < expect_value


def length_less_than_or_equals(check_value, expect_value):
    """判断长度小于等于"""
    assert isinstance(expect_value, integer_types)
    assert len(check_value) <= expect_value


def contains(check_value, expect_value):
    """判断期望结果内容包含在实际结果中"""
    assert str(expect_value) in str(check_value)


def contained_by(check_value, expect_value):
    """判断实际结果包含在期望结果中"""
    assert str(check_value) in str(expect_value)


def startswith(check_value, expect_value):
    """检查响应内容的开头是否和预期结果内容的开头相等"""
    assert builtin_str(check_value).startswith(builtin_str(expect_value))


def endswith(check_value, expect_value):
    """检查响应内容的结尾是否和预期结果内容相等"""
    assert builtin_str(check_value).endswith(builtin_str(expect_value))
