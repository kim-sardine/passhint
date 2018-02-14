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
        ('service', 'service'),
        ('waiting', 'waiting'),
        ('rejected', 'rejected'),
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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="waiting")

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
        return self.rule_sets.latest('created_at')

    @property
    def get_tag_list(self):
        return self.tag.split(',')

    @staticmethod
    def get_lastest_by_name(site_name, include_waiting=False):
        
        # service 중인 site가 1순위
        site = Site.objects.filter(
                    Q(name = site_name) &
                    Q(status = 'service'))

        if site:
            site = site.latest('created_at')
            return site

        #  waiting status의 Site 까지 필요로 하는 요청이라면
        if include_waiting:
            site = Site.objects.filter(
                        Q(name = site_name) &
                        Q(status = 'waiting'))

            if site:
                site = site.latest('created_at')
                return site

        raise Site.DoesNotExist 

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


class RuleSet(TimeStampedModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='rule_sets')

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

    def __str__(self):
        return '{}-{}'.format(self.site, self.created_at)

    class Meta:
        ordering = ['-created_at']

    @staticmethod
    def get_count_recent_1day(user):
        date_from = timezone.now() - datetime.timedelta(days=1)
        recent_count = RuleSet.objects.filter(user=user, created_at__gte=date_from).count()
        return recent_count