import decimal
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import View, TemplateView
from rest_framework import generics
from .models import BookingClass, Room, ClassRoom, Building, Floor
from rest_framework import serializers
from .serializers import RoomSerializers, BookingClassSerializers, FloorSerializers, BuildingSerializers
from datetime import datetime

class GetAllBuilding(generics.ListAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializers


class GetFloorById(generics.ListAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializers
    def get_queryset(self):
        return Floor.objects.filter(building = self.kwargs['id']).order_by('id')
        
class GetRoomByFloorID(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers
    def get_queryset(self):
        return Room.objects.filter(floor = self.kwargs['id']).order_by('id')

class GetAllRoom(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers

class GetIdRoom(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    lookup_field = 'id'
    serializer_class = RoomSerializers


class BookingRoomall(generics.ListCreateAPIView):
    queryset = BookingClass.objects.all()
    serializer_class = BookingClassSerializers

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

def updateRoom(Dataobj, status):
    room = Room.objects.get(id=Dataobj.id)
    room.status = status
    room.save()
    print('update', room.id)
    return Dataobj

def updater():
        nowtime = timezone.now()
        now = datetime(nowtime.year,nowtime.month,nowtime.day,nowtime.hour,nowtime.minute,nowtime.second)
        data_waiting_booking = BookingClass.objects.all()
        # data_waiting_class = ClassRoom.objects.all()
        
        #Condition When Class Is End or Not In Class Time
        # NotUsedRoom = list(filter(lambda x: check_notinbetweendates(x.start_time,x.end_time,now), data_waiting_booking))+list(filter(lambda x: check_notinbetweendates(x.start_time,x.end_time,now), data_waiting_class))
        NotUsedRoom = list(filter(lambda x: check_notinbetweendates(x.start_time,x.end_time,now), data_waiting_booking))
        # print('NotUse',NotUsedRoom)
        updateNotUseRoom = list(map(lambda x: updateStatusRoom(x,"0"),NotUsedRoom))
        #end

        #Conditon When Class Will I Start
        # UseRoom = list(filter(lambda x: not check_notinbetweendates(x.start_time,x.end_time,now),data_waiting_booking))+list(filter(lambda x: not check_notinbetweendates(x.start_time,x.end_time,now),data_waiting_class))
        UseRoom = list(filter(lambda x: not check_notinbetweendates(x.start_time,x.end_time,now),data_waiting_booking))
        # print('Use',UseRoom)
        updateForUseRoom = list(map(lambda x: updateStatusRoom(x,"1"),UseRoom))
        # end

        # RoomNoClass
        data_room = Room.objects.all()
        data_prewait = list(filter(lambda x: queryEmptyRoom(x),data_room))
        # print(data_prewait)
        # noclass = list(filter(lambda x: x.rooms_booking == [],data_room))
        updateForNoClass = list(map(lambda x: updateRoom(x,"0"),data_prewait))
        #Not in ClassRoom & Not in BookingRoom


        return True
   
def queryEmptyRoom(data):
    set = BookingClass.objects.filter(room = data.id)
    if not set:
        print(set)
        return True
    return False