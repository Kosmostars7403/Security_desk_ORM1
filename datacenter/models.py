from django.db import models
from django.utils import timezone

def format_duration(duration):
    minutes = int((duration % 3600) // 60)
    hours = int(duration // 3600)
    seconds = int((duration %3600)%60)
    return '{}:{}:{}'.format(hours, minutes,seconds)


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
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )

    def get_duration(self):
        if self.leaved_at:
            duration = (self.leaved_at - self.entered_at).total_seconds()
            return duration
        else:
            enter_time = timezone.localtime(self.entered_at)
            duration = (timezone.localtime() - enter_time).total_seconds()
            return duration

    def is_visit_long(self, minutes=60):
      duration = self.get_duration() // 60
      return duration > minutes
