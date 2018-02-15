from django import template
from django.utils.safestring import mark_safe
from passhint.models import Rule

register = template.Library()

# input : Rule
# ouput : HTML (button?)
@register.filter
def get_html_rule(rule_string):

    rule_splited = rule_string.split('_')

    if rule_splited[0] == 'len':
        rule_string = '_'.join(rule_splited[0:2])

    try:
        rule = Rule.objects.get(name=rule_string)
    except Rule.DoesNotExist:
        return ''

    level = rule.level
    desc_short = rule.desc_short
    desc_en = rule.desc_en

    # 숫자 rule의 경우 내용 변환
    if rule_splited[0] == 'len':
        num = rule_splited[2]
        level = level.replace('{len}', num)
        desc_short = desc_short.replace('{len}', num)
        desc_en = desc_en.replace('{len}', num)

    html = '<button type="button" class="btn btn-'+ level +' btn-sm m-1" title="'+ desc_short +'">'+ desc_en +'</button>'

    return mark_safe(html)


@register.filter
def print_password_rule(value):
    html_list = []

    if value:
        rule_list = value.split('/')
        for rule in rule_list:
            rule_div = rule.split('_')
            
            rule_dict = deepcopy(check_dict[rule_div[0]][rule_div[1]])

            if rule_div[0] == 'len':
                rule_dict['display']['text'] = rule_dict['display']['text'].replace('{len}', rule_div[2])
                rule_dict['description_en'] = rule_dict['description_en'].replace('{len}', rule_div[2])

            html_list.append('<button type="button" class="btn btn-'+ rule_dict['display']['class'] +' btn-sm m-1" title="'+ rule_dict['description_en'] +'">'+ rule_dict['display']['text'] +'</button>')
    return mark_safe(''.join(html_list))

@register.filter
def url_target_blank(value):
    if value:
        url_name = value.replace('http://', '')
        url_name = url_name.replace('https://', '')
        if url_name[-1] == '/':
            url_name = url_name[:-1]
        t_url = '<a target="_blank" href="' + value + '">' + url_name + '</a>'
        return mark_safe(t_url)
    else:
        return 'no link yet'