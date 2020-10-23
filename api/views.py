import decimal
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import View, TemplateView
from rest_framework import generics
from .models import BookingClass, Room, ClassRoom
from rest_framework import serializers
from .serializers import RoomSerializers, BookingClassSerializers
from datetime import datetime


class GetAllRoom(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers

class GetIdRoom(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    lookup_field = 'id'
    serializer_class = RoomSerializers


class BookingRoomall(generics.ListCreateAPIView):
    queryset = BookingClass.objects.all()
    serializer_classs = BookingClassSerializers

class BookingRoomId(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookingClass.objects.all()
    lookup_field = 'id'
    serializer_class = BookingClassSerializers


class BookingRoomSerializer(serializers.ModelSerializer):
    class Meta: 
        model = BookingClass
        fields = '__all__'
    
class UpdaterRoom(generics.ListCreateAPIView):
    queryset = BookingClass.objects.all()
    serializer_class  = BookingRoomSerializer


def formatDateTime(datetimeData):
    return datetime(datetimeData.year,datetimeData.month,datetimeData.day,datetimeData.hour,datetimeData.minute,datetimeData.second,datetimeData.microsecond,)

def check_notinbetweendates(start,end,now):

    if( (now <= formatDateTime(end)) and (now >= formatDateTime(start)) ):
        return False
    return True

def updateStatusRoom(DataObjectDate,status):
    room = Room.objects.get(id=DataObjectDate.room.id)
    room.status = status
    room.save()
    return DataObjectDate

def updater():
        nowtime = timezone.now()
        now = datetime(nowtime.year,nowtime.month,nowtime.day,nowtime.hour,nowtime.minute,nowtime.second)
        data_waiting_booking = BookingClass.objects.all()
        data_waiting_class = ClassRoom.objects.all()
        
        #Condition When Class Is End or Not In Class Time
        NotUsedRoom = list(filter(lambda x: check_notinbetweendates(x.start_time,x.end_time,now), data_waiting_booking))+list(filter(lambda x: check_notinbetweendates(x.start_time,x.end_time,now), data_waiting_class))
        print('NotUse',NotUsedRoom)
        updateNotUseRoom = list(map(lambda x: updateStatusRoom(x,"0"),NotUsedRoom))
        #end

        #Conditon When Class Will I Start
        UseRoom = list(filter(lambda x: not check_notinbetweendates(x.start_time,x.end_time,now),data_waiting_booking))+list(filter(lambda x: not check_notinbetweendates(x.start_time,x.end_time,now),data_waiting_class))
        print('Use',UseRoom)
        updateForUseRoom = list(map(lambda x: updateStatusRoom(x,"1"),UseRoom))
        # end

        #Not in ClassRoom & Not in BookingRoom


        return True

class MainView(TemplateView):
    def get(self, request, **kwargs):
        latestdata = BookingClass.objects.latest('timestamp')
        return render(request, 'api\index.html',{
            'start_date': latestdata.start_time,
            'end_date': latestdata.end_time,
            'timestamp': latestdata.timestamp,
            'room': latestdata.room.room_name,
            'count': latestdata.count,
            'status':latestdata.room.status,
            'datetimenow':datetime.now()
        })

   
