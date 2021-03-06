from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.utils.translation import get_language

from .models import ReportSite, ReportRuleSet
from passhint.models import Site, Rule, RuleSet
from passhint.common import RULE_LIST

class ReportSiteForm(forms.ModelForm):
    class Meta:
        model = ReportSite
        fields = ('name', 'main_url')
        labels = {
            "name": _("Site Name"),
            "main_url": _("Main URL")
            }
        help_texts = {
            'name': 'ex) Github, Samsung, Facebook',
            'main_url': 'ex) www.google.com, www.passhint.info'
        }


    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data['name']

        name = slugify(name, allow_unicode=True)

        if Site.objects.filter(name=name).exists():
            raise forms.ValidationError(_("This site already exists"))

        cleaned_data['name'] = name
        return cleaned_data


class ReportRuleSetForm(forms.ModelForm):
    class Meta:
        model = ReportRuleSet
        fields = RULE_LIST

        help_texts = {
            'len_min': 'Remain Empty if no limit',
            'len_max': 'Remain Empty if no limit',
        }

    def __init__(self, *args, **kwargs):
        super(ReportRuleSetForm, self).__init__(*args, **kwargs)

        for rule_name in RULE_LIST:
            rule = Rule.objects.get(name=rule_name)
            self.fields[rule_name].label = rule.desc_ko.replace(': {len}', '').strip() if get_language() in ['ko-kr', 'ko'] else rule.desc_en.replace(': {len}', '').strip()

    def clean_len_min(self):
        len_min = self.cleaned_data.get('len_min')
        if len_min == 0:
            len_min = None
        return len_min

    def clean_len_max(self):
        len_max = self.cleaned_data.get('len_max')
        if len_max == 0:
            len_max = None
        return len_max

    def clean(self):
        cleaned_data = super().clean()

        # 하나라도 None 이 아니거나 True 라는 것은 뭐라도 했다는 거니까 Pass
        for k, v in cleaned_data.items():
            if v not in [None, False]:
                return cleaned_data

        raise forms.ValidationError(_("Please Do Something"))
