from rest_framework import serializers
from django.core.serializers import serialize
from .models import Room, BookingClass, Building, ClassRoom

class BookingClassSerializers(serializers.ModelSerializer):
    class Meta: 
        model = BookingClass
        fields = '__all__'

class ClassRoomSerializers(serializers.ModelSerializer):
    class Meta: 
        model = ClassRoom
        fields = '__all__'



class  RoomSerializers(serializers.ModelSerializer):
    rooms_booking = BookingClassSerializers(many=True)
    rooms_class = ClassRoomSerializers(many=True)
    # bookingclassroom = serializers.SerializerMethodField('get_booking')
    # def get_booking(self, obj):
    #     data = BookingClass.objects.filter(room = obj).values()
    #     serializer_class  = BookingClassSerializers
    #     return data


    class Meta:
        model = Room
        fields = [ 'id', 'room_name', 'floor','status', 'rooms_booking', 'rooms_class' ]

