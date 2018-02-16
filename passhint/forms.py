from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from .models import RuleSet, ReportSite


class SiteSearchForm(forms.Form):
    keyword = forms.CharField(
        max_length=30, 
        widget=forms.TextInput(
            attrs={'id':'search_name'}
            )
        )

    def clean_keyword(self):
        keyword = self.cleaned_data.get('keyword').strip()
        return slugify(keyword, allow_unicode=True)

class ReportSiteForm(forms.ModelForm):
    class Meta:
        model = ReportSite
        fields = ('name', 'main_url')
        # labels = {
        #     "title": "Service Name"
        #     }
        # help_texts = {
        #     'title': 'ex) Airasia, CGV, Github...'
        # }

class ReportRuleSetForm(forms.ModelForm):
    class Meta:
        model = RuleSet
        fields = ('len_min', 'len_max',
                    'exc_special','exc_space','exc_id','exc_same','exc_series','exc_id','exc_common',
                    'inc_special','inc_lower','inc_upper','inc_number','inc_letter')
        # labels = {
        #     "title": "Service Name"
        #     }
        # help_texts = {
        #     'title': 'ex) Airasia, CGV, Github...'
        # }
        
    def clean(self):
        
        cleaned_data = super().clean()

        # 하나라도 None 이 아니거나 True 라는 것은 뭐라도 했다는 거니까 Pass
        for k, v in cleaned_data.items():
            if v not in [None, False]:
                return cleaned_data

        raise forms.ValidationError(_("Please Do Something"))