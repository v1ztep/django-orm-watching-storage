from django.db import models
import datetime
from django.utils.timezone import localtime


def get_duration(visit):
    if visit.leaved_at is None:
        delta = localtime() - visit.entered_at
    else:
        delta = visit.leaved_at - visit.entered_at
    duration = datetime.timedelta(seconds=delta.total_seconds())
    return duration


def format_duration(duration):
    hours = int(duration.total_seconds() // 3600)
    minutes = int((duration.total_seconds() // 60) % 60)
    corrected_format_duration = '{}ч {}мин'.format(hours, minutes)
    return corrected_format_duration


def is_visit_long(visit, minutes=60):
    is_strange = get_duration(visit).total_seconds() >= minutes*60
    return is_strange


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved="leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )
