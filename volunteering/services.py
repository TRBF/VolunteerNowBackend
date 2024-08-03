from typing import List
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
        return get_object_or_404(queryset)

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
        if(type(instances) is List or type(instances) is models.QuerySet):
            if(len(instances)>1):
                return self.serialize_many(instances)
            else:
                return self.serialize_one(instances[0])
        else:
            return self.serialize_one(instances)


class VolunteerService(BaseService):
    
    def __init__(self):
        super().__init__(Volunteer, VolunteerSerializer)

    def get_events_of_volunteer(self, volunteer_id):
        eventService = EventService()
        volunteer: Volunteer = self.get_with_pk(volunteer_id)
        return eventService.serialize(volunteer.event_set.all()) 

class OrganiserService(BaseService):
    
    def __init__(self):
        super().__init__(Organiser, OrganiserSerializer)

    def get_events_of_organiser(self, organiser_id):
        eventService = EventService()
        organiser: Organiser = self.get_with_pk(organiser_id)
        return eventService.serialize(organiser.event_set.all()) 



class EventService(BaseService):
    
    def __init__(self):
        super().__init__(Event, EventSerializer)

    def get_event_volunteers(self, event_id):
        volunteerService = VolunteerService()
        event: Event = self.get_with_pk(event_id)
        return volunteerService.serialize(event.volunteers.all()) 

    def get_event_organisers(self, event_id):
        organiserService = OrganiserService()
        event: Event = self.get_with_pk(event_id)
        return organiserService.serialize(event.organisers.all()) 

    def add_event_volunteer(self, **data):
        volunteerService = VolunteerService()
        event: Event = self.get_with_pk(data["event_id"])
        volunteer: Volunteer = volunteerService.get_with_pk(data["volunteer_id"])
        return self.serialize(event.volunteers.add(volunteer))

    def add_event_organiser(self, **data):
        organiserService = OrganiserService()
        event: Event = self.get_with_pk(data["event_id"])
        organiser: Organiser = OrganiserService.get_with_pk(data["organiser_id"])
        return self.serialize(event.organisers.add(organiser))
class ExperienceService(BaseService):
    
    def __init__(self):
        super().__init__(Experience, ExperienceSerializer)

class NotificationService(BaseService):
    
    def __init__(self):
        super().__init__(Notification, NotificationSerializer)
