from django import forms

class SiteSearchForm(forms.Form):
    site_name = forms.CharField(
        max_length=30, 
        widget=forms.TextInput(
            attrs={'placeholder':'서비스 이름을 입력하세요', 'id':'search_name'}
            )
        )
