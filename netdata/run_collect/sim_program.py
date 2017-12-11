#!/home/ec2-user/anaconda3/bin/python


import logging
from datetime import datetime, timezone
from dateutil import tz
from os.path import basename, splitext
from netdata.workers import JSONStorage


def log_info(msg):
    """
    Print info log message.
    :params msg: message text.
    """
    logging.info(' ' + msg)


def log_debug(msg):
    """
    Print debug log message.
    :params msg: message text.
    """
    logging.debug(msg)


def epoch_utc(s):
    """
    Convert epoch seconds to utc DateTime object.
    :params s: epoch seconds.
    :return: corresponding DateTime object.
    """
    return datetime.fromtimestamp(s, timezone.utc)


def utc_epoch(u):
    """
    Convert utc DateTime object to epoch seconds.
    :params u: utc DateTime object.
    :return: corresponding epoch seconds.
    """
    return u.timestamp()


def date_time_str(s):
    """
    Convert date_time object into string.
    :param s: DateTime.
    :return: string representing date-time.
    """
    return '{:%Y-%m-%d %H:%M:%S}'.format(s)


def silk_str(s):
    """
    Convert date_time object into string for silk.
    :param s: DateTime.
    :return: string representing date-time.
    """
    return '{:%Y/%m/%d:%H}'.format(s)


class SimProgram(JSONStorage):
    """
    Simulation storage and access.
    """
    end_offset = 60  # seconds to allow flow collection 
    # generally corresponds to yaf active-timeout of maximum stream length
    # and idle-timout of idle time to stop stream

    def __init__(self, file_name, path=''):
        """
        Initialize.
        :params file_name: file name of sim; can contain path.
        :params path: extra path to file.
        """
        super().__init__(path=path, name=file_name)

    @property
    def short_name(self):
        """
        Short name of the sim.
        :return: string with name.
        """
        return splitext(basename(self.file))[0]

    @property
    def start_epoch(self):
        return self.get('start')

    @property
    def end_epoch(self):
        return self.start_epoch + self.duration + self.end_offset

    @property
    def start_utc(self):
        """
        Start time.
        :return: DateTime of start time in utc.
        """
        return epoch_utc(self.start_epoch)

    @property
    def end_utc(self):
        """
        End time.
        :return: DateTime of end time in utc.
        """
        return epoch_utc(self.end_epoch)

    @property
    def start_est(self):
        """
        Start time.
        :return: DateTime of start time in est time.
        """
        return self.start_utc.astimezone(tz.gettz('America/New_York'))

    @property
    def end_est(self):
        """
        End time.
        :return: DateTime of end time in est time.
        """
        return self.end_utc.astimezone(tz.gettz('America/New_York'))

