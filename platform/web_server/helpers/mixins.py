from django.db import models
from django.db.models import Q, QuerySet
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _

from helpers import exceptions
            

def overlaps_query(starts_at: datetime, ends_at: datetime) -> QuerySet:
    # TODO (per Peter)
    # Assuming that we have a timeframe X with SD=x_sd and ED=x_ed and we check whether a
    # second timeframe Y overlaps that has SD=y_sd and ED=y_ed. These are the criteria I've
    # noticed that we care about for overlaps:
    # - is y_sd within X
    # - is y_ed within X
    # - is y_sd earler than x_sd and y_ed later than x_ed
    # The above should be true in all cases because as soon as either the start or end is
    # encompassed by the existing timeframe, we are 100% we have an overlap.
    overlaps_start = (
        Q(starts_at__lt=ends_at) & Q(starts_at__gte=starts_at)
    )
    within = (
        Q(starts_at__lte=starts_at) & Q(ends_at__gt=ends_at)
    )
    encompasses = (
        Q(starts_at__gte=starts_at) & Q(ends_at__lt=ends_at)
    )
    overlaps_end = (
        Q(ends_at__lte=ends_at) & Q(ends_at__gt=starts_at)
    ) 
    return overlaps_start | within | encompasses | overlaps_end


class IntersectionsQuerySet(models.QuerySet):
    def overlaps(self, starts_at: datetime, ends_at: datetime) -> QuerySet:
        return self.filter(overlaps_query(starts_at, ends_at))


class TimeframeModelMixin(models.Model):
    """ 
    Mixin that implements a timeframe abstraction, allowing overlap detection between
    existing timeframes and a given start datetime (starts_at) and end datetime (ends_at)
    as well as validation ensuring any created timeframe's starts_at precedes its ends_at.
    """

    class Meta:
        abstract = True

    class IntersectionsManager(models.Manager):
        def get_queryset(self) -> QuerySet:
            return IntersectionsQuerySet(model=self.model, using=self._db)

        def overlaps(self, starts_at: datetime, ends_at: datetime) -> QuerySet:
            return self.filter(overlaps_query(starts_at, ends_at))

    starts_at = models.DateTimeField(
        help_text=_("The start datetime for this timeframe (inclusive)"),
        null=True,
    )
    ends_at = models.DateTimeField(
        help_text=_("The end datetime for this timeframe (exclusive)"),
        null=True,
    )

    objects = models.Manager()
    intersections = IntersectionsManager()

    def save(self, **kwargs):
        if self.starts_at and self.ends_at and self.starts_at > self.ends_at:
            raise exceptions.TimeframeError()
        super().save(**kwargs)


class TimestampedModelMixin(models.Model):
    """ 
    Mixin that provides created and updated at fields
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
