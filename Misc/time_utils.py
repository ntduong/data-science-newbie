"""
Utilities for handling time in Python 2.x. 
See also, http://stackoverflow.com/questions/8777753/converting-datetime-date-to-utc-timestamp-in-python/8778548#8778548 for example.
"""
from datetime import date, datetime, timedelta, tzinfo
import calendar
import time

SECS_PER_DAY = 24*60*60
ZERO = timedelta(0)

class UTC(tzinfo):
    def utcoffset(self, dt):
        return ZERO
    
    def tzname(self, dt):
        return "UTC"
    
    def dst(self, dt):
        return ZERO
    
def create_UTC_datetime(year, month, day):
    utc = UTC()
    return datetime(year, month, day, tzinfo=utc)


def from_date_to_utc_timestamp(d, epoch=date(1970,1,1)):
    """ Convert from a date object (i.e., date(y,m,d) -> date object) to UTC timestamp
        Note: UTC timestamp (a.k.a., Unix time, POSIX time) is defined as 
              the number of seconds elapsed since 00:00:00 UTC, Jan 1, 1970 (Unix epoch)
        
        Return: UTC timestamp of given d. 
    """
    
    (d.toordinal() - epoch.toordinal()) * SEC_PER_DAYS
    
def from_datetime_to_utc_timestamp(dt, epoch=create_UTC_datetime(1970,1,1)):
    """ Convert from a datetime object to UTC timestamp, given the epoch as datetime(1970,1,1).
        Return: UTC timestamp of given dt.
    """
    
    return (dt-epoch).total_seconds()
    
def from_datetime_to_utc_timestamp2(dt):
    """ Given that dt is UTC datetime."""
    
    return calendar.timegm(dt.utctimetuple)
    
def get_tzinfo():
    """ Return
        + the offset of local (non-DST) timezone w.r.t UTC in seconds.
        + the name of local (non-DST/DST) timezone 
    """
    
    return time.timezone, time.tzname
    
if __name__ == "__main__":
    pass
    