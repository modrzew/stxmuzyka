from google.appengine.ext import ndb


class Result(ndb.Model):
    """
    Base result entity.
    """
    author = ndb.StringProperty()
    url = ndb.StringProperty()
    info = ndb.TextProperty()
    when = ndb.DateTimeProperty()
    date = ndb.DateProperty()
    time = ndb.TimeProperty()

    def _pre_put_hook(self):
        if self.when:
            self.date = self.when.date()
            self.time = self.when.time()

    def to_dict(self):
        return dict(
            id=self.key.id(),
            author=self.author,
            url=self.url,
            info=self.info,
            date=self.date.strftime('%Y-%m-%d'),
            time=self.time.strftime('%H:%M')
        )


class Config(ndb.Model):
    """
    Singleton config object.
    """
    last_refresh = ndb.DateTimeProperty()

    @classmethod
    def get_master(cls):
        return cls.get_or_insert('master')
