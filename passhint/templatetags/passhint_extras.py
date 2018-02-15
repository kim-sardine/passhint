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