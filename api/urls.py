from django.conf.urls import url
from django.urls import path,include

from . import views
urlpatterns = [
    path('room', views.GetAllRoom.as_view()),
    path('room/<int:id>',views.GetIdRoom.as_view()),
    path('bookingroom', views.BookingRoomall.as_view()),
    path('bookingroom/<int:id>',views.BookingRoomId.as_view()),
    url(r'^$', views.MainView.as_view())
]