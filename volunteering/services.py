from typing import List
from django.db import models
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from django.apps import apps
from rest_framework import serializers
import typing
from .models import Experience, Event, Volunteer, Organiser, Notification
from api.serializers import ExperienceSerializer, EventSerializer, VolunteerSerializer, OrganiserSerializer, NotificationSerializer
from django.contrib.postgres.search import SearchVector

M = typing.TypeVar("M", bound=type[models.base.Model])
S = typing.TypeVar("S", bound=serializers.SerializerMetaclass)


class BaseService(typing.Generic[M, S]):

    def __init__(self, model: M, serializer: S):
        self._model: M = model
        self._serializer: S = serializer 

    def get_all(self):
        return self._model.objects.all()

    def get_with_pk(self, pk: int) -> M:
        try:
            instance: M = self._model.objects.filter(pk=pk) 
            return instance[0]        

        except self._model.DoesNotExist:
            raise Http404("Given query not found...") 

    def get_where(self, **object_data) -> M:
        try:
            instances: M = self._model.objects.filter(**object_data) 
            return instances        
        except self._model.DoesNotExist:
            raise Http404("Given query not found...") 

    def add(self, **object_data):
        self._model.objects.create(**object_data)

    def add_from_request_data(self, request_data):
        serializer = self._serializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
        
        return serializer.data

    def delete(self, object):
        return object.delete() 

    def delete_with_pk(self, pk):
        object = self.get_with_pk(pk)
        self.delete(object)

    def search(self, query, match_rule, *fields):
        search_query = None
        for field in fields:
            q = models.Q(**{f"{field}__{match_rule}": query })
            if search_query:
                search_query = search_query | q 
            else:
                search_query = q
        results = self._model.objects.filter(search_query)
        return results 


    def serialize_one(self, instance):
        return self._serializer(instance).data

    def serialize_many(self, instances):
        return self._serializer(instances, many=True).data

    def serialize(self, instances):

        if(type(instances) is List or type(instances) is models.QuerySet):
            if(len(instances)>1):
                return self.serialize_many(instances)
            elif(len(instances)>0):
                return self.serialize_one(instances[0])
            else:
                return {} 
        else:
            return self.serialize_one(instances)



class VolunteerService(BaseService):
    
    def __init__(self):
        super().__init__(Volunteer, VolunteerSerializer)

    def get_events_of_volunteer(self, volunteer_id):
        volunteer: Volunteer = self.get_with_pk(volunteer_id)
        return volunteer.event_set.all() 

    def get_volunteer_notifications(self, volunteer_id):
        volunteer: Volunteer = self.get_with_pk(volunteer_id)
        return volunteer.notifications.all()

    def get_volunteer_experiences(self, volunteer_id):
        volunteer: Volunteer = self.get_with_pk(volunteer_id)
        return volunteer.experiences.all()

class OrganiserService(BaseService):
    
    def __init__(self):
        super().__init__(Organiser, OrganiserSerializer)

    def get_events_of_organiser(self, organiser_id):
        organiser = self.get_with_pk(organiser_id)
        return organiser.event_set.all() 



class EventService(BaseService):
    
    def __init__(self):
        super().__init__(Event, EventSerializer)

    def get_event_volunteers(self, event_id):
        event: Event = self.get_with_pk(event_id)
        return event.volunteers.all() 

    def get_event_organisers(self, event_id):
        event: Event = self.get_with_pk(event_id)
        return event.organisers.all() 

    def add_event_volunteer(self, **data):
        volunteerService = VolunteerService()
        event: Event = self.get_with_pk(data["event_id"])
        volunteer: Volunteer = volunteerService.get_with_pk(data["volunteer_id"])
        return event.volunteers.add(volunteer)

    def add_event_organiser(self, **data):
        organiserService = OrganiserService()
        event: Event = self.get_with_pk(data["event_id"])
        organiser: Organiser = organiserService.get_with_pk(pk=data["organiser_id"])
        return event.organisers.add(organiser)

class ExperienceService(BaseService):
    
    def __init__(self):
        super().__init__(Experience, ExperienceSerializer)

class NotificationService(BaseService):
    
    def __init__(self):
        super().__init__(Notification, NotificationSerializer)


class SearchService:
    
    # def search(self, query, *model_names):
    #     result = models.QuerySet()
    #     model_list = app.get_models()
    #     for available_model in model_list:
    #         for queried_model in model_names:
    #             if(available_model==queried_model):
    #                 result+=available_model.get_where()

    def search(self, query):
        eventService = EventService()
        volunteerService = VolunteerService()
        organiserService = OrganiserService()
        
        results = list() 
        
        results.append({"events": eventService.serialize(eventService.search(query, "istartswith", "name"))}) 
        results.append({"volunteers": volunteerService.serialize(volunteerService.search(query, "istartswith", "username", "first_name", "last_name"))})
        results.append({"organisers": organiserService.serialize(organiserService.search(query, "istartswith", "name"))})
    
        return results
    
    def search_tag(self, tag):
        eventService = EventService()
        volunteerService = VolunteerService()
        organiserService = OrganiserService()
        
        results = list() 
        
        results.append({"events": eventService.serialize(eventService.search(tag, "icontains", "name", "description"))}) 
        results.append({"volunteers": volunteerService.serialize(volunteerService.search(tag, "icontains", "username", "first_name", "last_name"))})
        results.append({"organisers": organiserService.serialize(organiserService.search(tag, "icontains", "name"))})
        
        return results
