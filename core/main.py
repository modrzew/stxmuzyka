from webapp2 import Route, WSGIApplication
import api
import api_admin
import views


app = WSGIApplication([
    # Views
    Route('/', views.MainHandler, name='Main'),
    # API
    Route('/api/results', api.ResultsHandler, name='Results'),
    # Admin
    Route('/admin', views.AdminHandler, name='Admin'),
    Route('/admin/api/result/<result_id:\d+>', api_admin.ResultHandler, name='Result'),
], debug=True)
