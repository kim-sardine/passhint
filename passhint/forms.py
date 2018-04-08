from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

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

class InlinePwCheckForm(forms.Form):

    pw = forms.CharField(
        max_length=50, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Check if you can use your password in this site.'),
                'id':'inline_pw_check'
                }
            )
        )