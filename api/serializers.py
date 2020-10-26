from rest_framework import serializers
from django.core.serializers import serialize
from .models import Room, BookingClass, Building, ClassRoom, Floor

class BuildingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'

class FloorSerializers(serializers.ModelSerializer):
    # building_of_floor = BuildingSerializers(many=True)
    class Meta:
        model = Floor
        fields = '__all__'


class BookingClassSerializers(serializers.ModelSerializer):
    class Meta: 
        model = BookingClass
        fields = '__all__'

class ClassRoomSerializers(serializers.ModelSerializer):
    class Meta: 
        model = ClassRoom
        fields = '__all__'



class  RoomSerializers(serializers.ModelSerializer):
    rooms_booking = BookingClassSerializers(many=True,read_only=True)
    rooms_class = ClassRoomSerializers(many=True, read_only=True)
    # bookingclassroom = serializers.SerializerMethodField('get_booking')
    # def get_booking(self, obj):
    #     data = BookingClass.objects.filter(room = obj).values()
    #     serializer_class  = BookingClassSerializers
    #     return data


    class Meta:
        model = Room
        fields = [ 'id', 'room_name', 'floor','status', 'rooms_booking', 'rooms_class' ]

