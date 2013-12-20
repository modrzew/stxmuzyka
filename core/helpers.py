from datetime import timedelta, tzinfo


# Timezones
class CEST(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=1)

    def tzname(self, dt):
        return "CEST"

    def dst(self, dt):
        return timedelta(hours=1)


class UTC(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(hours=0)
