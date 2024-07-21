from django.utils.timezone import datetime, now, timedelta
import pytest

from helpers.time_period import TimePeriod

#################################
# Time period 
#################################
def test_timeperiod_with_no_start_or_end_includes_all_datetimes():
    period = TimePeriod(None, None)
    assert period.within(now())
    assert period.within(now() + timedelta(days=100000))
    assert period.within(now() - timedelta(days=100000))

def test_timeperiod_with_only_start():
    start = now()
    period = TimePeriod(start, None)
    assert period.within(start)
    assert period.within(start + timedelta(days=100000))
    assert not period.within(start - timedelta(days=1))

def test_timeperiod_with_only_end():
    end = now()
    period = TimePeriod(None, end)
    assert period.within(end)
    assert period.within(end - timedelta(days=100000))
    assert not period.within(end + timedelta(days=1))

def test_timeperiod_with_start_and_end():
    start = now()
    end = start + timedelta(days=2)
    period = TimePeriod(start, end)
    assert not period.within(start - timedelta(days=1))
    assert period.within(start)
    assert period.within(start + timedelta(days=1))
    assert period.within(start + timedelta(days=2))
    assert not period.within(start + timedelta(days=3))
