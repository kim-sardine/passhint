import re
from copy import deepcopy
from .models import Rule

def pw_check(pw, rule_list):
    '''
    password 와 password_rule 을 입력받은 후 가능한 password 인지 여부와 불가능하다면 왜 불가능한지 리턴
    '''
    result = '' # success, warning, fail, error
    message = {
        'error_en' : [],
        'error_ko' : [],
        'warning_en' : [],
        'warning_ko' : [],
    }
    if pw and rule_list:

        result = 'success'
        
        for rule_name in rule_list:

            rule = Rule.get_rule_by_name(rule_name)

            if rule.regex is None:
                message['warning_en'].append(rule.error_en)
                message['warning_ko'].append(rule.error_ko)
                if result == 'success':
                    result = 'warning'
                
                continue

            p = re.compile(rule.regex)
            m = p.search(pw)

            if (m and not rule.regex_result) or (not m and rule.regex_result): # 매칭되어야 하는데 되지 않았거나 매칭되지 않아야 하는데 매칭되면 error
                result = 'fail'
                message['error_en'].append(rule.error_en)
                message['error_ko'].append(rule.error_ko)
    else:
        result = 'error'

    return (result, message)