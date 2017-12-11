from datetime import datetime, timezone, timedelta


class DateTime:
    """
    Date-time class supporting automatic conversions to epoch time.
    """
    _date_time = None  # datetime object

    def __init__(self, year=1970, month=1, day=1,
                 hour=0, minute=0, second=0, tzinfo=timezone.utc,
                 epoch=-1,
                 date_str='', time_str='', datetime_obj=None):
        """
        Initialize with epoch time if given, otherwise
        with date and time strings if given, otherwise
        with datetime_obj if give, otherwise
        year, month, day, hour, minute, second.
        :param year: year.
        :param month: month.
        :param day: day.
        :param hour: hour.
        :param minute: minute.
        :param second: second.
        :param tzinfo: timezone.
        :param epoch: epoch time.
        :param date_str: date in the format year-month-day = %Y-%m-%d.
        :param time_str: time in the format hour:minute:second
        = %H:%M:%S
        :param datetime_obj: datetime object
        """
        if epoch >= 0:
            self._date_time = datetime.fromtimestamp(epoch, tzinfo)
        elif date_str and time_str:
            d = date_str.strip() + ' ' + time_str.strip()
            self._date_time = datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
        elif datetime:
            self._date_time = datetime_obj
        else:
            self._date_time = datetime(year, month, day,
                                       hour, minute, second, tzinfo)

    @property
    def epoch(self):
        """
        Epoch time.
        :return: epoch time in seconds.
        """
        return self._date_time.timestamp()

    def __str__(self):
        """
        String representation.
        :return: string representation.
        """
        return '{:%Y-%m-%d %H:%M:%S}'.format(self._date_time)

    def __add__(self, other):
        """
        Add a time delta.
        :param other: seconds or datetime.timedelta object.
        """
        if isinstance(other, timedelta):
            shifted = self._date_time + other
        else:
            shifted = self._date_time + timedelta(seconds=other)
        return DateTime(datetime_obj=shifted)

