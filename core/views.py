from ext.handlers import BaseHandler


class MainHandler(BaseHandler):
    """
    Base handler.
    I'm using Angular to do everything frontendy, so one is more than enough.
    """
    def get(self):
        ctx = dict(
            is_admin='false'
        )
        self.render('index.html', context=ctx)


class AdminHandler(BaseHandler):
    """
    Admin handler. Will set window.stx.isAdmin to true.
    """
    def get(self):
        ctx = dict(
            is_admin='true'
        )
        self.render('index.html', context=ctx)
