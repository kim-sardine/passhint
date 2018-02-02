from django.db import models
from django.conf import settings
from django.forms import URLField

def url_validator(url):

    url_form_field = URLField()
    try:
        url = url_form_field.clean(url)
    except ValidationError:
        raise ValidationError('Invalid URL Type')


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Site(TimeStampedModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, unique=True)
    rule_set = models.ForeignKey('RuleSet',blank=True, null=True, on_delete=models.SET_NULL)
    tag = models.CharField(max_length=200)
    hit = models.BigIntegerField(default=0)
    main_url = models.CharField(max_length=100, validators=[url_validator])

    def __str__(self):
        return name


class Rule(TimeStampedModel):

    LEVEL_CHOICES = (
        ('success', 'success'),
        ('info', 'info'),
        ('warning', 'warning'),
        ('danger', 'danger'),
    )

    name = models.CharField(max_length=50, unique=True)
    regex = models.CharField(max_length=200)
    regex_result = models.BooleanField()
    desc_ko = models.CharField(max_length=200)
    desc_en = models.CharField(max_length=200)
    desc_short = models.CharField(max_length=200)
    error_ko = models.CharField(max_length=200)
    error_en = models.CharField(max_length=200)
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES)

    def __str__(self):
        return '{}-{}'.format(name, desc_short)


class RuleSet(TimeStampedModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    len_min = models.SmallIntegerField(blank=True, null=True)
    len_max = models.SmallIntegerField(blank=True, null=True)
    
    exc_special = models.NullBooleanField(default=None)
    exc_space = models.NullBooleanField(default=None)
    exc_id = models.NullBooleanField(default=None)
    exc_same = models.NullBooleanField(default=None)
    exc_series = models.NullBooleanField(default=None)
    exc_id = models.NullBooleanField(default=None)
    exc_common = models.NullBooleanField(default=None)
    
    inc_special = models.NullBooleanField(default=None)
    inc_lower = models.NullBooleanField(default=None)
    inc_upper = models.NullBooleanField(default=None)
    inc_number = models.NullBooleanField(default=None)
    inc_letter = models.NullBooleanField(default=None)