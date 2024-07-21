import pytest
from pytest import raises

from django.utils.timezone import now, timedelta

from helpers import exceptions
from helpers.mixins import TimeframeModelMixin


##################################################
# A timeframe's starts_at must preceed its ends_at
##################################################
def test_creating_timeframe_succeeds(
        timeframe_model: TimeframeModelMixin.__class__,
):
    n = now()
    timeframe_model.objects.create(starts_at=n, ends_at=n+timedelta(hours=1))


def test_creating_timeframe_with_starts_at_not_preceeding_ends_at_fails(
        timeframe_model: TimeframeModelMixin.__class__,
):
    n = now()
    with raises(exceptions.TimeframeError):
        timeframe_model.objects.create(starts_at=n, ends_at=n-timedelta(minutes=1))


##################################################
# Test overlaps calculation
##################################################
def test_overlap_with_no_timeframes_does_not_exist(
        timeframe_model: TimeframeModelMixin.__class__,
):
    assert not timeframe_model.objects.exists()
    starts_at = now() - timedelta(days=100000)
    ends_at = starts_at + timedelta(days=200000)
    assert not timeframe_model.intersections.overlaps(starts_at, ends_at).exists()


@pytest.mark.django_db
def test_assert_raises_with_overlapping_beginning(
        timeframe_model: TimeframeModelMixin.__class__,
):
    existing_starts_at = now()
    existing_ends_at = existing_starts_at + timedelta(hours=1)
    timeframe_model.objects.create(
        starts_at=existing_starts_at,
        ends_at=existing_ends_at,
    )
    new_starts_at = existing_starts_at - timedelta(minutes=30)
    new_ends_at = existing_starts_at + timedelta(minutes=30)
    assert new_starts_at < existing_starts_at < new_ends_at < existing_ends_at
    assert timeframe_model.intersections.overlaps(new_starts_at, new_ends_at).exists()


@pytest.mark.django_db
def test_assert_raises_with_overlapping_end(
        timeframe_model: TimeframeModelMixin.__class__,
):
    existing_starts_at = now()
    existing_ends_at = existing_starts_at + timedelta(hours=1)
    timeframe_model.objects.create(
        starts_at=existing_starts_at,
        ends_at=existing_ends_at,
    )
    new_starts_at = existing_starts_at + timedelta(minutes=30)
    new_ends_at = existing_ends_at + timedelta(minutes=30)
    assert existing_starts_at < new_starts_at < existing_ends_at < new_ends_at
    assert timeframe_model.intersections.overlaps(new_starts_at, new_ends_at).exists()


@pytest.mark.django_db
def test_assert_raises_when_both_timestamps_within_timeframe(
        timeframe_model: TimeframeModelMixin.__class__,
):
    existing_starts_at = now()
    existing_ends_at = existing_starts_at + timedelta(hours=1)
    timeframe_model.objects.create(
        starts_at=existing_starts_at,
        ends_at=existing_ends_at,
    )
    new_starts_at = existing_starts_at + timedelta(minutes=1)
    new_ends_at = existing_ends_at - timedelta(minutes=1)
    assert existing_starts_at < new_starts_at < new_ends_at < existing_ends_at
    assert timeframe_model.intersections.overlaps(new_starts_at, new_ends_at).exists()


@pytest.mark.django_db
def test_assert_raises_when_timestamps_encompass_timeframe(
        timeframe_model: TimeframeModelMixin.__class__,
):
    existing_starts_at = now()
    existing_ends_at = existing_starts_at + timedelta(hours=1)
    timeframe_model.objects.create(
        starts_at=existing_starts_at,
        ends_at=existing_ends_at,
    )
    new_starts_at = existing_starts_at - timedelta(minutes=1)
    new_ends_at = existing_ends_at + timedelta(minutes=1)
    assert new_starts_at <  existing_starts_at < existing_ends_at < new_ends_at
    assert timeframe_model.intersections.overlaps(new_starts_at, new_ends_at).exists()
