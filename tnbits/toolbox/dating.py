# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#            dating.py
#

import datetime
from time import localtime
from random import randint
import re

def uniqueLong():
    """The `uniqueLong` method answers a unique number (as string) of 18
    digits."""
    return DateTime.timestamprandomlong()

def timestampLong():
    """The `timestampLong` method answers the timestamp. This may not be
    unique."""
    return DateTime.timestamplong()

def uniqueId(size=0):
    """The `uniqueId` method answers a unique number (as string) of _size_
    length concatenated timestamps. Minimum length of the number is 18 digits,
    or else string will not be unique."""
    n = ''
    size = max(size,18)

    while len(n) < size:
        n += str(uniqueLong())
    return n[:size]

def leapyear(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def monthdays(year, month):
    # Separate method, so it also can be used on initialization
    if month == 2:
        if leapyear(year):
            return 29
        else:
            return 28
    elif month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    else:
        return 30

def checkdatetime(date):
    """The `checkdatetime` answers the _date_ if it is a date. If date is None,
    then answer None. If date is a string, then convert to DateTime. Check on
    the month and day boundaries. Answer the same type that date was. Note that
    we do not check if date was already a DateTime. This method is especially
    made to set database fields with dates, where that None will result in a
    NULL value for that field."""
    if not date: # Check on None or empty string
        return None
    if not isinstance(date, DateTime):
        return DateTime(date=date).date
    return date

def newdatetime(date):
    """The `newdate` method answers a new `DateTime` instance. If the _date_ is
    `None`, then answer `None`. If _date_ is a string, then convert to
    `DateTime`. Check on the month and day boundaries."""
    if date is None:
        return None
    if not isinstance(date, DateTime):
        date = DateTime(date=date)
    return date

class Duration:
    """The `Duration` class contains a duration in time. It can e.g. be used to
    add to a `DateTime` instance with a new date as result.

    ```
    Duration(3)
    Duration(seconds=10)
    Duration(td=timedelta)
    ```

    All common arithmetic applies to a `Duration` instance.

    ```
    d = Duration(3)
    d * 3 is a duration of 6 days.
    ```
    """
    def __init__(self, days=0, seconds=0, microseconds=0, milliseconds=0,
            minutes=0, hours=0, weeks=0, td=None):
        """If td is already there, then use it and ignore all other
        parameters."""
        if td is not None:
            self.timedelta = td
        else:
            self.timedelta = datetime.timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)

    def __getattr__(self, key):
        if key == 'days':
            return self.timedelta.days
        if key == 'seconds':
            return self.timedelta.seconds
        return self.__dict__[key]

    def __len__(self):
        return self.days

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if self.days:
            return 'Duration(%dd,%ds)' % (self.days, self.seconds)
        return 'Duration(%ds)' % self.seconds

    # To be added __iter__

    def __coerce__(self, p):
        return None

    def __nonzero__(self):
        return True

    def __mul__(self, n):
        return Duration(days=self.days * n, seconds=self.seconds * n)

    def __div__(self, n):
        return Duration(days=self.days / n, seconds=self.seconds / n)

    def __neg__(self):
        return Duration(days= -self.days, seconds= -self.seconds)

    def __iadd__(self, item):
        return self + item

    def __isub__(self, item):
        return self - item

    def __imul__(self, item):
        return self * item

    def __idiv__(self, item):
        return self / item

    def __add__(self, value):
        # Duration + Date = Date
        # Duration + Duration = Duration
        # Duration + 3 = Duration
        if isinstance(value, int):
            return Duration(days=self.days + value, seconds=self.seconds)
        if isinstance(value, Duration):
            return Duration(days=self.days + value.days, seconds=self.seconds + value.seconds)
        if isinstance(value, DateTime):
            return DateTime(dt=value.datetime + self.timedelta)
        raise ValueError('[Duration.__add__] Illegal type to add to a Duration instance "%s"' % value)

    def __sub__(self, dt):
        # Duration - Date = Date
        # Duration - Duration = Duration
        # Duration - 3 = Duration
        if isinstance(dt, int):
            return Duration(days=self.days - dt, seconds=self.seconds)
        if isinstance(dt, Duration):
            return Duration(days=self.days - dt.days, seconds=self.seconds - dt.seconds)
        if isinstance(dt, DateTime):
            return DateTime(dt=dt.datetime - self.timedelta)
        raise ValueError('[Duration.__add__] Illegal type to subtract from a Duration instance "%s"' % dt)

    def min(self):
        """Most negative timedelta object that can be represented."""
        return datetime.timedelta.min

    def max(self):
        """Most positivie timedelta object that can be represented."""
        return datetime.timedelta.max

    def resolution(self):
        """Smallest resolvable difference that a timedelta object can
        represent."""
        return datetime.timedelta.resolution

Period = Duration    # Make the lib backward compatible. But the use of Period is supported.

class DateTime:
    """The `newdate` method answers a new `DateTime` instance. If the _date_ is
    `None`, then answer `None`. If _date_ is a string, then convert to
    `DateTime`. Check on the month and day boundaries.

    * Initialize the current date if the _date_ is equal to `now`
    * Initialize on first day of the week if year and week are defined
    * Initialize from existing datetime if "dt" is defined
    * Initialize from _date_time_ string, date and time separated by white space.
    * Initialize from _date_ string (identical to the result of self.date) if defined
    * Initialize from _time_ string (identical to the result of self.time) if defined
    * Initialize from (year, month, day) if all of them are defined.
    * Otherwise raise an error

    If the _trimvalues_ attribute is set to `False` (default is `True`) then
    the input values of the date are *not* trimmed to their minimum and
    maximum values. This checking is done in context for days in months and
    years.

    ```
    DateTime(date='now')
    DateTime(date='2008-11-23')
    DateTime(date='2008-11-23', time='23:11')
    DateTime(date='2008-11-23', time='23:11:22')
    DateTime(2008, 11, 23)
    DateTime(2008, 11, 23, 23, 11, 22, 0)
    DateTime(2008, week=23)
    ```
    """
    keys = {'year': 0, 'month': 1, 'day': 2, 'hour': 3, 'minute': 4, 'second': 5, 'weekday': 6, 'yearday': 7, 'tz': 8}
    daynames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    fulldaynames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    monthnames = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    fullmonthnames = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    def __init__(self, year=None, month=None, day=None, hour=0, minute=0, second=0, microsecond=0, tz=None,
        dt=None, date_time=None, date=None, time=None, week=None, trimvalues=True, mtime=None):

        if dt is not None:
            # Assume that dt is of type date string. Direct init from existing datetime
            self.datetime = dt
        else:
            if date == 'now':
                self.datetime = datetime.datetime.now()
                return

            if date_time is not None:
                date_time = str(date_time) # In case of a datetime instance from Django
                datetimeparts = date_time.split(' ')
                date = datetimeparts[0].strip()
                time = datetimeparts[1].strip()

            if date is not None:
                if isinstance(date, (str, unicode)):
                    # Could one of the follovwing formats
                    # YYYY-MM-DD HH:MM:SS
                    stamp = re.compile("(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)([\-\+]\d+)?")
                    m = stamp.match(date)
                    if m:
                        year = int(m.group(1))
                        month = int(m.group(2))
                        day = int(m.group(3))
                        hour = int(m.group(4))
                        minute = int(m.group(5))
                        second = int(m.group(6))
                        #@# tz must be a tzinfo object, not an integer, leave it as None for now.
                        #tz = int(m.group(7) or tz)
                    else:
                        try:
                            if '.' in date or '/' in date:
                                date = date.replace('.', '-').replace('/', '-')
                            date = date.split(' ')[0]    # Skip possible time part of date input
                            year, month, day = date.split('-')
                            if int(day) > int(year):    # If notation 25-03-2007, then swap day and year
                                year, day = day, year
                        except:
                            raise ValueError('[DateTime] Wrong date format "%s"' % date)
                else:
                    # If date is an integer .... format: YYYYMMDD
                    d = str(date)
                    year, month, day = d[:4], d[4:6], d[6:]

            if mtime is not None:
                # Evaluate the number of seconds since the beginning of time
                tt = localtime(mtime)
                year = tt.tm_year
                month = tt.tm_mon
                day = tt.tm_mday
                hour = tt.tm_hour
                minute = tt.tm_min
                second = tt.tm_sec

            if time is not None:
                time = time.split(' ')[-1]    # Skip possible date part of the time input
                timeparts = time.split(':')
                if len(timeparts) == 2:
                    hour, minute = timeparts
                    second = 0
                elif len(timeparts) == 3:
                    hour, minute, second = timeparts

            if year is not None and week is not None:
                week = int(week)
                # Set date of first day in the requested week
                dt = datetime(int(year), 1, 1) + datetime.timedelta(weeks=week)
                self.datetime = dt - datetime.timedelta(days=dt.timetuple()[self.keys['weekday']])
                # This algorithm may be one week off, so test and adjust if it does not match.
                if self.week > week:
                    self.datetime -= datetime.timedelta(days=7)

            elif year is None or month is None or day is None:
                if time is not None:
                    # Just a time was specified,
                    year = month = day = 0
                else:
                    raise ValueError('[DateTime] Did not supply all values of y,m,d (%s,%s,%s)' % (year, month, day))

            elif trimvalues:
                year          = int(year)
                month          = min(12, max(1, int(month)))
                day          = min(monthdays(year, month), max(1, int(day)))
                hour          = min(23, max(0, int(hour)))
                minute          = min(60, max(0, int(minute)))
                second         = min(60, max(0, int(second)))
                microsecond     = min(99, max(0, int(microsecond)))
                self.datetime = datetime.datetime(year, month, day, hour, minute, second, microsecond, tz)
            else:
                self.datetime = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second),
                                                int(microsecond), tz)

    def __getattr__(self, key):
        if key in self.keys:
            # year, month, day, hour, minute, second, weekday, yearday
            return self.datetime.timetuple()[self.keys[key]]

        method = '_' + key
        if hasattr(self, method):
            return getattr(self, method)()

        return self.__dict__[key]

    def __str__(self):
        """The function `str(dt)` answers the string representation of the
        date. Typically the identical to `dt.date + ' ' + dt.te`.
        """
        return repr(self)

    def __repr__(self):
        """The function `repr(dt)` (or ``dt``) answers the string
        representation of the date, typically identical to `dt.date + ' ' +
        dt.te`.
        """
        return self.date + ' ' + self.time

    def __nonzero__(self):
        """Always answer `True` indicating that a `DateTime` instance can never
        be zero."""
        return True

    def __lt__(self, dt):
        """Answers `True` if `self` is in the past of date `dt` as in `self
        > dt`.  Note that in evaluating the condition the difference in time
        is taken into account as well.  Use `self.datenumber > dt.datenumber`
        to test on date comparison only instead of `dy &amp;lt; self`.g """
        return self.datetime < dt.datetime

    def __le__(self, dt):
        """Answers `True` if `self` is in the past of or equal to date `dt` as
        in `self >= dt`.  Note that in evaluating the condition the difference
        in time is taken into account as well.  Use `self.datenumber >
        dt.datenumber` to test on date comparison only instead of `dy >= self`.
        """
        return self.datetime <= dt.datetime

    def __gt__(self, dt):
        return self.datetime > dt.datetime

    def __ge__(self, dt):
        return self.datetime >= dt.datetime

    def __ne__(self, dt):
        return not self == dt

    def __eq__(self, dt):
        if isinstance(dt, DateTime):
            return self.datetime == dt.datetime
        return False

    def __coerce__(self, duration):
        return None

    def __iadd__(self, item):
        return self + item

    def __isub__(self, item):
        return self - item

    def __add__(self, duration):
        """Add the _duration_ to `self`.

        ```
        Date + Duration = Date
        Date + 3 = Date
        ```
        """
        if isinstance(duration, (int, float)):
            duration = Duration(days=duration)
        assert isinstance(duration, Duration)
        return DateTime(dt=self.datetime + duration.timedelta)

    def __sub__(self, durationordate):
        """
        ```
        Date - Duration = Date
        Date - Date = Duration
        Date - 3 = Date
        """
        if isinstance(durationordate, (int, float)):
            durationordate = Duration(days=durationordate)
        if isinstance(durationordate, Duration):
            # Date - Duration = Date
            return DateTime(dt=self.datetime - durationordate.timedelta)
        if isinstance(durationordate, DateTime):
            # Date - Date = Duration
            return Duration(td=self.datetime - durationordate.datetime)

    @classmethod
    def now(cls):
        return cls(date='now')

    @classmethod
    def timestamprandomlong(cls):
        """The `_uniquenumber` method/attributes answers a unique number of
        format `'20090621200511993066'`,derived from date, time and a six digit
        random number. This can be used e.g. in a URL as parameters to make
        sure that browser will not cache the content of the page. The number is
        also used to create a unique file name for background shell scrts.
        """
        return cls.timestamplong() + ('%06d' % randint(0, 999999))

    @classmethod
    def timestamplong(cls):
        import time
        return '%012d' % int(time.time()*100)

    def _timestamp(self, usetz=False):
        """The `dt.timestamp` answers a formatted string `2010-10-05
        16:47:29+o4` of the date. This is exactly what SQL needs as timestamp
        with time zone definion.

        NOTE: use of tz does not yet work, and is ignored.
        """
        if self.tz is None or not usetz:
            tz = ""
        elif self.tz < 0:
            tz = "-%02d" % -self.tz
        else:
            tz = "+%02d" % self.tz
        return  "%s %s%s" % (self.date, self.time, tz)

    def _date(self):
        """The `dt.date` answers a formatted string `2008-10-23` of the date.
        This is exactly what SQL needs as date-string definion.
        """
        return '%04d-%02d-%02d' % (self.year, self.month, self.day)

    def _eurodate(self):
        """The `dt.eurodate` answers a formatted string `23-10-2008` of the
        date."""
        return '%02d-%02d-%02d' % (self.day, self.month, self.year)

    def _studyyear(self):
        """The `dt.studyyear` method/attribute answers a string `0708 with
        leading zero for the study year from `2007-08-01` until `2008-031`
        """
        studyyear = (self.year - 2000) * 100 + self.year - 2000 + 1
        if self.month <= 8: # Switch study year on end of summer break
            studyyear -= 101
        return '%04d' % studyyear

    def _datenumber(self):
        """The `dt.datenumber` method/attribute answers a long integer number
        20080502 of the date. This can by used to compare dates on day only and
        not on time. Or it can be used as ordering key."""
        return self.year * 10000 + self.month * 100 + self.day

    def _datetuple(self):
        """The `dt.datetuple` method/attribute answers a tuple `(y,m,d)` of the
        date."""
        return self.year, self.month, self.day

    def _time(self):
        """The `dt.datenumber` method/attribute answers a formatted
        `'12:23:45'` time string."""
        return '%02d:%02d:%02d' % (self.hour, self.minute, self.second)

    def _date_time(self):
        """The `dt.date_time` method/attribute answers a formatted `'2010-12-06
        12:23:34'` date/time stng.
        """
        return '%s %s' % (self.date, self.time)

    def _timetuple(self):
        """The `dt.timetuple` method/attribute answers a tuple `(h, m, s)` of
        the time."""
        return self.hour, self.minute, self.second

    def _timezone(self):
        """The `dt.timezone` method/attribute answers the timezone `dt.tz`.
      """
        return self.tz

    def _week(self):
        """The `dt.week` method/attribute answers the weeknummer according to
        ISO 8601 where the first week of the year that contains a thursday.
        """
        return self.datetime.isocalendar()[1]

    def _dayname(self):
        """The `dt.dayname` method/attribute answers a 3 letter abbreviation of
        current day name."""
        return self.daynames[self.weekday]

    def _fulldayname(self):
        """The `dt.fulldayname` method/attribute answers the full name of the
        current day."""
        return self.fulldaynames[self.weekday]

    def _monthname(self):
        """The `dt.monthname` method/attribute answers a 3 letter abbreviation
        of current month name."""
        return self.monthnames[self.month]

    def _fullmonthname(self):
        """The `dt.fullmonthname` method/attribute answers the full name of the
        current month."""
        return self.fullmonthnames[self.month]

    def _monthstart(self):
        """The `dt.monthstart` method/attribute answers the first day of the
        current month."""
        return self + (1 - self.day) # Keep integer calculation combined by brackets

    def _monthend(self):
        """The `dt.monthend` method/attribute answers the last day of the
        current month."""
        return self - self.day + self.monthdays

    def _weekstart(self):
        """The `dt.weekstart` method/attribute answers the “Monday” date of the
        current week."""
        return self - self.weekday

    def _weekend(self):
        """Keep integer calculation combined by brackets."""
        return self + (7 - self.weekday)

    def _yearstart(self):
        """The `dt.yearstart` method/attribute answers the first day of the
        current year."""
        return DateTime(self.year, 1, 1)

    def _yearend(self):
        """The `dt.yearend` method/attribute answers the last day of the
        current year."""
        return DateTime(self.year, 12, 31)

    def _workday(self):
        """The `dt.workday` method/attribute answers `True` if this day is one
        of Monday till Friday."""
        return 0 <= self.weekday <= 4

    def _nextworkday(self):
        """The `dt.nextworkday` method/attribute answers the first next date
        (including itself) that is a workday."""
        if self.workday:
            return self
        return self + (7 - self.weekday) # Keep integer calculation combined by brackets

    def _leapyear(self):
        """The `dt.leapyear` method/attribute answers a boolean if the `dt` is
        a leap year."""
        return leapyear(self.year)

    def _yeardays(self):
        """The `dt.yeardays` method/attribute answers the number of days in the
        current year."""
        if leapyear(self.year):
            return 366
        return 365

    def _monthdays(self):
        """The `dt.monthdays` method/attribute answers the number of days in
        the current month."""
        return monthdays(self.year, self.month)

    def _nextmonth(self):
        """The `nextmonth` method/attribute answers the first day of the month
        after the current month. Due to length differences between the months,
        it is not consistent to answer the current day number in the next
        month, so it is set to 1."""
        return self + (self.monthdays - self.day + 1)

    def _prevmonth(self):
        """The `prevmonth` method/attribute answers the first day of the month
        previous to the current month.  Due to length differences between the
        months, it is not consistent to  answer the current day number ithe
        previous month."""
        return (self.monthstart - 1).monthstart

    def _calendarmonth(self):
        """The `calendarmonth` method/attribute answers a list of lists
        containing the weeks with dates of the current month. Note that the
        first and lost week are filled with the days of end of the previous
        month and the start of the next month.

        ```
            [
                [p01, p02, p03, d01, d02, d03, d04],
                [d05, d06, d07, d08, d09, d10, d11],
                [d12, d13, d14, d15, d16, d17, d18],
                [d19, d20, d21, d22, d23, d24, d25],
                [d26, d27, d28, d29, d30, n01, n02]
            ]
        ```
        """
        monthweekdates = []
        weekstart = self.monthstart.weekstart
        running = False
        while not running or weekstart.month == self.month:
            weekdates = []
            monthweekdates.append(weekdates)
            for day in range(7):
                weekdates.append(weekstart + day)
            weekstart += 7
            running = True
        return monthweekdates

    def _calendaryear(self):
        """The `calendaryear` method/attribute answers a list of lists of lists
        containing all `calendarmonths` of the year.

        ```
            [
            [
                [p01, p02, p03, d01, d02, d03, d04],
                [d05, d06, d07, d08, d09, d10, d11],
                [d12, d13, d14, d15, d16, d17, d18],
                [d19, d20, d21, d22, d23, d24, d25],
                [d26, d27, d28, d29, d30, n01, n02]
            ]
            [
            ...
            ]
            ...
            ]
        ```
        """
        yearweekdates = []
        for month in range(1, 13):
            yearweekdates.append(DateTime(year=self.year, month=month, day=1).calendarmonth)
        return yearweekdates

    def nextdaynamed(self, weekday):
        if not (0 <= weekday <= 7):
            raise ValueError('[DateTime.nextdaynamed] Weekday "%s" must be in range (0, 8)' % weekday)
        nextday = self + Duration(days=1)
        while 1:
            if nextday.weekday == weekday:
                return nextday
            nextday = nextday + Duration(days=1)
        return None

if __name__ == "__main__":
    print(DateTime(year=1900, month=1, day=1, hour=0, minute=0, second=1110000))
    p = Duration(seconds=10) * 6 / 2
    print('Duration', p,)
    print('Negated duration', -p)
    print('Duration 1 day longer', p + 1)
    print('Duration 2 minutes longer', p + Duration(minutes=2))
    d1 = DateTime(date='now')
    d2 = d1 + Duration(seconds=10)

    print(d1.weekday, d1.dayname)
    print(d1.month, d1.monthname)
    print(d1.week, d2.week)
    print('Next working day', d1.nextworkday)
    print(d1)
    print(d1 + p)
    print('6 days later', d1 + 6)
    print('60 days later', d1 + 60)
    print('First work day after 60 days', (d1 + 60).nextworkday)
    print('20 days earlier', d1 - 20)
    print(d1 - p)
    print(d1 - d2 + d2)
    print(d1.date)
    print(d1.datenumber)
    print(d1.datetuple)
    print(d1.time)
    print(d1.timetuple)
    print(d1.nextdaynamed(5).dayname)
    print(d1.nextdaynamed(5).nextworkday.dayname)
    print(d1.nextdaynamed(6).nextworkday.dayname)
    print(d1.leapyear)
    d3 = DateTime(2007, 12, 20)
    print(d3.nextmonth)
    d3 = DateTime(2008, 1, 15)
    print(d3.prevmonth)
    print(d3 - d1)
    d3 = DateTime(d1.year, d1.month, 1)
    print(d3 + Duration(days=d3.monthdays - 1))
    print(d1.monthstart, d1.monthend)
    print(d1 - Duration(days=1))
    print('First week of this month', DateTime(date='2007-12-10').monthstart.week)
    print('Date of start of first week of this month', DateTime(date='2007-12-10').monthstart.weekstart)
    print('Previous month of 2007-12-10 is', DateTime(date='2007-12-10').prevmonth.date)
    print('Previous month of 2008-1-10 is', DateTime(date='2008-1-10').prevmonth.date)
    print('Next month of 2007-12-10 is', DateTime(date='2007-12-10').nextmonth.date)
    print('Next month of 2008-1-10 is', DateTime(date='2008-1-10').nextmonth.date)
    print('First day of third week', DateTime(year=2008, week=2).date)
    print('Trim day value', DateTime(year=2008, month=2, day=35).date)
    print('Trim month and day value', DateTime(year=2008, month=22, day=35).date)
    print('Year start and end', d1.yearstart.date, d1.yearend.date)
    print('Month start and end', d1.monthstart.date, d1.monthend.date)
    print(d1.calendarmonth)
    print(DateTime(date='2008-2-29').calendarmonth)
    print(DateTime(date='2007-12-31').calendaryear)
