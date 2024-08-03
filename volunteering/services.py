from django.db import models
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import serializers

from .models import Experience, Event, Volunteer, Organiser, Notification
from api.serializers import ExperienceSerializer, EventSerializer, VolunteerSerializer, OrganiserSerializer, NotificationSerializer


class BaseService():

    def __init__(self, model, serializer):
        self._model: models.base.Model = model
        self._serializer: serializers.SerializerMetaclass = serializer 

    def get_all(self):
        return self._model.objects.all()

    def get_with_pk(self, pk):
        queryset = self._model.objects.filter(pk=pk) 
        return get_list_or_404(queryset)

    def get_where(self, **object_data):
        queryset = self._model.objects.filter(**object_data) 
        return get_list_or_404(queryset) 

    def add(self, **object_data):
        self._model.objects.create(**object_data)

    def add_from_request_data(self, request_data):
        serializer = self._serializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
        return serializer.data

    def delete(self, object):
        object.delete() 

    def delete_with_pk(self, pk):
        object = self.get_with_pk(pk)
        self.delete(object)

    def serialize_one(self, instance):
        return self._serializer(instance).data

    def serialize_many(self, instances):
        return self._serializer(instances, many=True).data

    def serialize(self, instances):
        if(len(instances)>1):
            return self.serialize_many(instances)
        else:
            return self.serialize_one(instances[0])


class VolunteerService(BaseService):
    
    def __init__(self):
        super().__init__(Volunteer, VolunteerSerializer)


class EventService(BaseService):
    
    def __init__(self):
        super().__init__(Event, EventSerializer)

class ExperienceService(BaseService):
    
    def __init__(self):
        super().__init__(Experience, ExperienceSerializer)

class NotificationService(BaseService):
    
    def __init__(self):
        super().__init__(Notification, NotificationSerializer)
