from django.conf.urls import url
from django.urls import path,include

from . import views
urlpatterns = [
    path('room', views.GetAllRoom.as_view()),
    path('room/<int:id>', views.GetIdRoom.as_view()),
    path('room/floor/<int:id>', views.GetRoomByFloorID.as_view()),

    path('bookingroom', views.BookingRoomall.as_view()),
    path('bookingroom/<int:id>',views.BookingRoomId.as_view()),
    
    path('building', views.GetAllBuilding.as_view()),

    path('floor/<int:id>', views.GetFloorById.as_view()),
    
]