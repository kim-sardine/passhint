from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from .models import Site, RuleSet

class SiteSearchForm(forms.Form):
    site_name = forms.CharField(
        max_length=30, 
        widget=forms.TextInput(
            attrs={'placeholder':'서비스 이름을 입력하세요', 'id':'search_name'}
            )
        )

    def clean_site_name(self):
        site_name = self.cleaned_data.get('site_name').strip()
        return slugify(site_name, allow_unicode=True)

class ReportSiteForm(forms.ModelForm):
    class Meta:
        model = Site
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