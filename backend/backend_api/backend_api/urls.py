from django.contrib import admin
from django.urls import path
from apis import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/' ,views.home),
    path('api/signal', views.getSignalInfo),
    path('api/multiple', views.getMultipleInfo)
]
