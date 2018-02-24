from django.db import models
from django.conf import settings
from django.forms import URLField
from django.utils.text import slugify
from django.forms import ValidationError
from django.utils import timezone
from django.db.models import Q

import datetime

def url_validator(url):

    url_form_field = URLField()
    try:
        url = url_form_field.clean(url)
    except ValidationError:
        raise ValidationError('Invalid URL Type')

STATUS_CHOICES = (
        ('waiting', 'waiting'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
        ('late', 'late'),
    )

class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Site(TimeStampedModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=60)
    tag = models.CharField(max_length=200, blank=True, null=True)

    hit = models.BigIntegerField(default=0)
    main_url = models.CharField(max_length=100, validators=[url_validator])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        
        self.name = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def get_rule_set_list(self):
        return self.rule_sets.first()

    @property
    def get_tag_list(self):
        return self.tag.split(',')

    # 태그가 완전 일치하는 사이트가 하나 존재하면 site 리턴
    # 존재하지 않거나 복수 존재하면 None 리턴
    @classmethod
    def get_site_by_tag(cls, keyword):
        sites = cls.objects.all()
        
        result = []
        for site in sites:
            tag_list = site.get_tag_list
            if keyword in tag_list:
                result.append(site)

        if len(result) == 1:
            return result[0]
        else:
            return None

class Rule(TimeStampedModel):

    LEVEL_CHOICES = (
        ('success', 'success'),
        ('info', 'info'),
        ('warning', 'warning'),
        ('danger', 'danger'),
    )

    name = models.CharField(max_length=50, unique=True)
    regex = models.CharField(max_length=200, blank=True, null=True)
    regex_result = models.NullBooleanField()
    desc_ko = models.CharField(max_length=200)
    desc_en = models.CharField(max_length=200)
    desc_short = models.CharField(max_length=200)
    error_ko = models.CharField(max_length=200)
    error_en = models.CharField(max_length=200)
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES)

    def __str__(self):
        return '{}-{}'.format(self.name, self.desc_short)


class BaseRuleSet(models.Model):

    len_min = models.SmallIntegerField(blank=True, null=True)
    len_max = models.SmallIntegerField(blank=True, null=True)
    
    exc_special = models.BooleanField(default=False)
    exc_space = models.BooleanField(default=False)
    exc_id = models.BooleanField(default=False)
    exc_same = models.BooleanField(default=False)
    exc_series = models.BooleanField(default=False)
    exc_id = models.BooleanField(default=False)
    exc_common = models.BooleanField(default=False)
    
    inc_special = models.BooleanField(default=False)
    inc_lower = models.BooleanField(default=False)
    inc_upper = models.BooleanField(default=False)
    inc_number = models.BooleanField(default=False)
    inc_letter = models.BooleanField(default=False)

    class Meta:
        abstract = True


class RuleSet(TimeStampedModel, BaseRuleSet):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='rule_sets')

    def __str__(self):
        return '{}-{}'.format(self.site, self.created_at)

    class Meta:
        ordering = ['-created_at']

    # XXX RULE SENSITIVE
    @property
    def get_true_rule_list(self):
        
        result = []
        
        if self.len_min is not None:
            result.append('len_min_'+str(self.len_min))
        
        if self.len_max is not None:
            result.append('len_max_'+str(self.len_max))
        
        if self.exc_special is True:
            result.append('exc_special')

        if self.exc_space is True:
            result.append('exc_space')
        
        if self.exc_id is True:
            result.append('exc_id')
        
        if self.exc_same is True:
            result.append('exc_same')
        
        if self.exc_series is True:
            result.append('exc_series')
        
        if self.exc_common is True:
            result.append('exc_common')
        
        if self.inc_special is True:
            result.append('inc_special')
        
        if self.inc_lower is True:
            result.append('inc_lower')
        
        if self.inc_upper is True:
            result.append('inc_upper')
        
        if self.inc_number is True:
            result.append('inc_number')
        
        if self.inc_letter is True:
            result.append('inc_letter')

        return result

