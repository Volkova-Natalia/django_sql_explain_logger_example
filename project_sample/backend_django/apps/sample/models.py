from django.db import models
from django.urls import reverse
from django.forms.models import model_to_dict


class People(models.Model):
    first_name = models.CharField(
        null=False, blank=False, unique=False,
        max_length=255,
        verbose_name='First name',
        help_text='First name of the person')
    last_name = models.CharField(
        null=False, blank=False, unique=False,
        max_length=255,
        verbose_name='Last name',
        help_text='Last name of the person')

    class Meta:
        indexes = [
            models.Index(fields=['last_name'], name='idx_last_name')
        ]

    # --------------------------------------------------

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    def get_absolute_url(self):
        return reverse('sample' + ':' + 'person', args=[self.id])

    # --------------------------------------------------

    def to_dict(self, *, fields=None, exclude=None):
        return model_to_dict(instance=self, fields=fields, exclude=exclude)

    # --------------------------------------------------
