from django.urls import path
from lx220 import views
app_name = "lx220"
urlpatterns = [
    path('home/', views.indexlogin),
    path('check/', views.login1),
    path('main/', views.indexmain),
    path('main2/<data2>', views.indexmain2),
    path('test/', views.test),
    path('main1/<data1>', views.indexmain1),
    path('main3/<data3>/<data4>/<data5>/<data6>', views.indexmain3),
    path('main4/<data5>/<data6>', views.indexmain4),
    path('main5/<data7>', views.indexmain5),
    path('upload/<data8>', views.uploadindex),
    path('download/<data9>/<data10>', views.downloadindex)
]