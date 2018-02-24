from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from .models import ReportSite, ReportRuleSet
from passhint.models import Site, Rule, RuleSet

class ReportSiteForm(forms.ModelForm):
    class Meta:
        model = ReportSite
        fields = ('name', 'main_url')
        labels = {
            "name": "Site Name",
            "main_url": "Main URL"
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

# XXX RULE SENSITIVE
class ReportRuleSetForm(forms.ModelForm):
    class Meta:
        model = ReportRuleSet
        fields = [rule.name for rule in Rule.objects.all()]

        labels = {
            rule.name:rule.label for rule in Rule.objects.all()
        }
        help_texts = {
            'len_min': 'Remain Empty if no limit',
            'len_max': 'Remain Empty if no limit',
        }

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
