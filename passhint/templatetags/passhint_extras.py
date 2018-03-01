from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from passhint.models import Rule

register = template.Library()

# input : Rule
# ouput : HTML (button?)
@register.simple_tag
def get_html_rule(rule_list, field):

    result = ''
    for rule_string in rule_list:
        html = get_html_rule_each(rule_string, field)
        result += html
    return mark_safe(result)


@register.simple_tag
def get_html_rule_each(rule_string, field):
    
    rule_splited = rule_string.split('_')

    if rule_splited[0] == 'len':
        rule_string = '_'.join(rule_splited[0:2])

    try:
        rule = Rule.objects.get(name=rule_string)
    except Rule.DoesNotExist:
        return ''

    desc_short = rule.desc_short
    desc_en = rule.desc_en
    desc_ko = rule.desc_ko
    guide_ko = rule.guide_ko
    guide_en = rule.guide_en

    # 숫자 rule의 경우 내용 변환
    if rule_splited[0] == 'len':
        try:
            num = rule_splited[2]
        except:
            num = '123'
        desc_short = desc_short.replace('{len}', num)
        desc_en = desc_en.replace('{len}', num)
        desc_ko = desc_ko.replace('{len}', num)
        guide_ko = guide_ko.replace('{len}', num)
        guide_en = guide_en.replace('{len}', num)


    # display version 에 따라 형식 변경. 기본은 영어
    text = desc_en
    guide = guide_en

    if field == 'ko':
        text = desc_ko
        guide = guide_ko
    elif field == 'short':
        text = desc_short

    html = '<button type="button" class="btn btn-'+ rule.level +' btn-sm m-1" data-toggle="popover" data-placement="top" data-trigger="focus" data-content="' + guide + '">'+ text +'</button>'

    return mark_safe(html)


# TODO URL 부분은 믿을만한 library 이용하기
@register.filter
def get_anchor_tag(url):

    if url:
        # http, https 가 없으면 a tag 가 정상동작하지 않으므로 넣어준다
        if 'http://' not in url and 'https://' not in url:
            url = 'http://'+url

        # 사용자에게 보여주기 위한 url 생성 (보기 좋게)
        url_shown = url.replace('http://', '')
        url_shown = url_shown.replace('https://', '')
        if url_shown[-1] == '/':
            url_shown = url_shown[:-1]

        t_url = '<a target="_blank" href="' + url + '">' + url_shown + '</a>'
        return mark_safe(t_url)
    else:
        return 'no link yet'
