from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.conf import settings

from passhint.common import POINT_DICT
from log.models import LogPoint


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    point = models.BigIntegerField(default=0)

    def set_point(self, key):
        # POINT 부여
        self.point = F('point') + POINT_DICT[key]
        self.save()
        self.refresh_from_db()

        # LOG 저장
        LogPoint.save_log_point(self.user, POINT_DICT[key], key)