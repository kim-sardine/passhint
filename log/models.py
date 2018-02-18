from django.db import models
from django.conf import settings
from passhint.models import Site

STATUS_CHOICES = (
        ('waiting', 'waiting'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
    )

class LogSite(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.site.name

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def save_log_site(cls, site, user):
        log = cls(site=site)
        if user:
            log.user = user
        log.save()

class LogSearch(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    keyword = models.CharField(max_length=30, blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword

    @classmethod
    def save_log_search(cls, user, keyword, result):

        log = cls(keyword=keyword)
        if user:
            log.user = user

        if result:
            try:
                name = result.name
            except AttributeError: # Many result
                name = []
                for site in result:
                    name.append(site.name)
                name = ','.join(name)
            
            log.result = name

        log.save()