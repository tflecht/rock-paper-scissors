from datetime import datetime
import pytz
import time


# https://www.youtube.com/watch?v=5rJBnFWbQGk
# Format       Preview                          Indicator
# -------------------------------------------------------
# Short Time   4:20 AM                          t
# Long Time    4:20:00 AM                       T
# Short Date   05/10/2017                       d
# Long Date    May 10, 2017                     D
# Short Full   May 10, 2017 4:20 AM             f
# Long Full    Wednesday, May 10 2017 4:20 AM   F
# Relative     4 Years Ago                      R


def short_full_from_isoformat(iso_string: str) -> str:
    if not iso_string:
        return 'unscheduled'
    dt = utc_datetime_from_isoformat(iso_string)
    unix_timestamp = int(time.mktime(dt.timetuple()))
    return f"<t:{unix_timestamp}:f>"


def utc_datetime_from_isoformat(iso_string: str) -> datetime:
    dt = datetime.fromisoformat(iso_string)
    utc_dt = dt.astimezone(pytz.utc)
    return utc_dt
