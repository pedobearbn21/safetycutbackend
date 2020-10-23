from django.db import models
from datetime import datetime 
from django.utils import timezone


# Create your models here.
class Building(models.Model):
    building_name = models.CharField(max_length=255)
    def __str__(self):
        return f'Building :{self.building_name}'
    
class Floor(models.Model):
    floor_name = models.CharField(max_length=20)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    def __str__(self):
        return f'Building :{self.building.building_name}, Floor: {self.floor_name}'
    
    class Meta:
        ordering = ['floor_name']

status_choices = [("0","off"),("1","on")]
class Room(models.Model):
    room_name = models.CharField(max_length=10)
    hardware_id = models.CharField(max_length=255)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    status = models.CharField(max_length=255,choices=status_choices,default="0")
    def __str__(self):
        return f' Building : {self.floor.building.building_name}, Floor : {self.floor.floor_name}, Room: {self.room_name}'

# class BookingRoom(models.Model):
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.timestamp = datetime.utcnow()
    #     return super(BookingRoom, self).save(*args, **kwargs)
    # class_room = models.ManyToManyField()

class ClassRoom(models.Model):
    class_name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rooms_class')
    timestamp = models.DateTimeField(default=None)
    def __str__(self):
        return f' Time Duration {self.start_time} ---->  {self.end_time}, Room  {self.room.room_name} Status {self.room.status}'
    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()
        return super(ClassRoom, self).save(*args, **kwargs)

class BookingClass(models.Model):
    class_name = models.CharField(max_length=255, default='')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    count = models.IntegerField(default=0)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rooms_booking')
    timestamp = models.DateTimeField(default=None)
    def __str__(self):
        return f' Time Duration {self.start_time} ---->  {self.end_time}, Room  {self.room.room_name}  Status {self.room.status}'
    def save(self, *args, **kwargs):
        self.count = self.count+1
        self.timestamp = timezone.now()
        return super(BookingClass, self).save(*args, **kwargs)