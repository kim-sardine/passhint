from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

import datetime

from passhint.models import Site, TimeStampedModel, BaseRuleSet, url_validator, STATUS_CHOICES


class ReportRuleSet(TimeStampedModel, BaseRuleSet):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='report_rule_sets')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="waiting")

    def __str__(self):
        return '{}-{}'.format(self.site, self.created_at)

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def get_count_recent_1day(cls, user):
        date_from = timezone.now() - datetime.timedelta(days=1)
        recent_count = cls.objects.filter(user=user, created_at__gte=date_from).count()
        return recent_count


class ReportSite(TimeStampedModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="waiting")
    main_url = models.CharField(max_length=100, validators=[url_validator])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
