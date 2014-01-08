# coding: utf-8
from datetime import datetime, time, timedelta
import re

from google.appengine.api import urlfetch

from core.helpers import CEST, UTC
from core.models import Result, Config


# Where to grab logs from
LOG_URL = 'http://logs.pagenoare.net/%%23stxnext-muzyka/%s.log'
URL_REGEX = re.compile(
    'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
    re.I
)
AUTHOR_REGEX = re.compile('^(\d{2}):(\d{2}) (@|)\s+?(\S+?) │', re.I)
# Logs have this weird offset
TIME_DELTA = timedelta(minutes=15)


def parse(day):
    """
    Parses log file from given day in search for URLs.
    Returns list of Result entities.
    """
    config = Config.get_master()
    # Timezones! \o/
    if config.last_refresh:
        last_refresh_utc = config.last_refresh.replace(tzinfo=UTC())
        last_refresh = last_refresh_utc.astimezone(CEST())
    else:
        last_refresh = None
    # Fetching
    url = LOG_URL % day.strftime('%Y-%m-%d')
    log = urlfetch.fetch(url)
    lines = log.content.splitlines()
    results = []
    # Parsing
    for line in lines:
        urls = URL_REGEX.findall(line)
        if not urls:
            continue
        time_author = AUTHOR_REGEX.search(line)
        if not time_author:
            continue
        when = None
        if time_author:
            author = time_author.group(4)
            when_t = time(int(time_author.group(1)), int(time_author.group(2)))
            when_naive = datetime.combine(day, when_t) + TIME_DELTA
            when = when_naive.replace(tzinfo=CEST())
        if last_refresh and when and when < last_refresh:
            continue
        # More timezones \o/
        when = when.replace(tzinfo=None)
        # Remove URLs...
        info = URL_REGEX.sub('', line)
        # Author and time...
        info = AUTHOR_REGEX.sub('', info)
        # and leave all other info
        info = info.strip()
        for url in urls:
            result = Result(
                url=url,
                author=author,
                info=info,
                when=when
            )
            results.append(result)
    return results
