from django.contrib.auth.models import User
from django.db import models
from django.http.response import Http404
from rest_framework import serializers
import typing

from rest_framework.relations import ObjectTypeError

from .models import UserProfile, Opportunity, Participation, Callout, Application, UserAddedParticipation, Question
from api.serializers import OpportunitySerializer, UserProfileSerializer, ParticipationSerializer, CalloutSerializer, ApplicationSerializer, QuestionSerializer, UserAddedParticipationSerializer, UserSerializer

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
        print(self._model)
        try:
            instances: M = self._model.objects.filter(**object_data) 
            return instances        
        except self._model.DoesNotExist:
            raise Http404("Given query not found...") 

    def add(self, **object_data):
        return self._model.objects.create(**object_data)

    def add_from_request_data(self, request_data):
        serializer = self._serializer(data=request_data)
        print(f'\nData: {request_data}')
        if serializer.is_valid():
            instance = serializer.save()
            return self._serializer(instance).data
        else:
            print(serializer.errors)
            return serializer.errors

    def update(self, pk, object_data):
        return self._model.objects.filter(pk=pk).update(**object_data)

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

        if(type(instances) is list or type(instances) is models.QuerySet):
            if(len(instances)>1):
                return self.serialize_many(instances)
            elif(len(instances)>0):
                return self.serialize_one(instances[0])
            else:
                return {} 
        else:
            return self.serialize_one(instances)

class ParticipationService(BaseService):
    
    def __init__(self):
        super().__init__(Participation, ParticipationSerializer)

    def add_participation(self, **request_data):
        user = request_data["user_id"]
        opportunity = request_data["opportunity_id"]
        
        del request_data["user_id"]
        del request_data["opportunity_id"]
        
        request_data.update({"user": user, "opportunity": opportunity})
        
        return self.add_from_request_data(request_data)

    def get_user_participations(self, id):
        return self.get_where(user=id)      

class UserService(BaseService):
    
    def __init__(self):
        super().__init__(User, UserSerializer)

class UserProfileService(BaseService):
    
    def __init__(self):
        super().__init__(UserProfile, UserProfileSerializer)

    def get_user_opportunities(self, user_id):
        participationService = ParticipationService()
        opportunityService = OpportunityService()
        participations = participationService.get_where(user_id=user_id) 
        opportunities = [opportunityService.get_with_pk(participation.opportunity_id) for participation in participations]

        return opportunities 

    def get_user_callouts(self, user_id):
        user: UserProfile = self.get_with_pk(user_id)

        return user.callout_set.all() 


    def update_user_pfp(self, user_id, request):
        user: UserProfile = self.get_with_pk(user_id)
        print("PFP!!!", request.data["profile_picture"])
        
        if user.profile_picture:
            user.profile_picture.delete(save = False)

        # try: 
        user.profile_picture = request.data["profile_picture"]
        user.save()
        return("Success!")
        # except:
            # return("User not found (probably).")
        


    def update_user_cover(self, user_id, request):
        user: UserProfile = self.get_with_pk(user_id)
        
        if user.cover_image:
            user.cover_image.delete(save = False)

        try: 
            user.profile_picture = request.FILES["cover_image"]
            user.save()
            return("Success!")
        except:
            return("User not found (probably).")

class OpportunityService(BaseService):
    
    def __init__(self):
        super().__init__(Opportunity, OpportunitySerializer)

    def get_opportunity_volunteers(self, opportunity_id):
        participationService = ParticipationService()
        userService = UserProfileService()
        participations = participationService.get_where(opportunity_id=opportunity_id, role="volunteer") 
        users = [userService.get_with_pk(participation.user_id) for participation in participations]

        return users 

    def get_opportunity_organisers(self, opportunity_id):
        participationService = ParticipationService()
        userService = UserProfileService()
        participations = participationService.get_where(opportunity_id=opportunity_id, role="organiser") 
        organisers = [userService.get_with_pk(participation.user_id) for participation in participations]

        return organisers 


    def update_opportunity_pfp(self, opportunity_id, request):
        opportunity: Opportunity = self.get_with_pk(opportunity_id)
        opportunity.profile_picture = request.FILES.get("profile_picture")
        opportunity.save()
        return("Success!")
        # try: 
        #     opportunity.profile_picture = request.FILES.get("profile_picture")
        #     opportunity.save()
        #     return("Success!")
        # except e:
        #     return("Opportunity not found (probably).") 


    def update_opportunity_cover(self, opportunity_id, request):
        opportunity: Opportunity = self.get_with_pk(opportunity_id)

        try: 
            opportunity.cover_image = request.FILES.get("cover_image")
            opportunity.save()
            return("Success!")
        except:
            return("Opportunity not found (probably).") 

    def update_opportunity_post_image(self, opportunity_id, request):
        opportunity: Opportunity = self.get_with_pk(opportunity_id)

        try: 
            opportunity.post_image = request.FILES.get("post_image")
            opportunity.save()
            return("Success!")
        except:
            return("Opportunity not found (probably).") 

class ApplicationService(BaseService):
    
    def __init__(self):
        super().__init__(Application, ApplicationSerializer)
 
class QuestionService(BaseService):
    
    def __init__(self):
        super().__init__(Question, QuestionSerializer)   

class UserAddedParticipationService(BaseService):
    
    def __init__(self):
        super().__init__(UserAddedParticipation, UserAddedParticipationSerializer)

    def update_participation_picture(self, user_id, request):
        userAddedParticipation: UserAddedParticipation = self.get_with_pk(user_id)
        
        if userAddedParticipation.participation_picture:
            userAddedParticipation.participation_picture.delete(save = False)

        try: 
            userAddedParticipation.participation_picture = request.FILES.get("participation_picture")
            userAddedParticipation.save()
            return("Success!")
        except:
            return("User not found (probably).")

    def update_participation_diploma(self, user_id, request):
        userAddedParticipation: UserAddedParticipation = self.get_with_pk(user_id)
        
        if userAddedParticipation.diploma:
            userAddedParticipation.diploma.delete(save = False)

        try: 
            userAddedParticipation.diploma = request.FILES.get("diploma")
            userAddedParticipation.save()
            return("Success!")
        except:
            return("userAddedParticipation not found (probably).")

class SearchService:

    def search(self, query):
        userService = UserService()
        userProfileService = UserProfileService()
        
        results = list() 
        results += userService.serialize(userService.search(query, "istartswith", "username", "first_name", "last_name"))
        results += userProfileService.serialize(userProfileService.search(query, "istartswith", "description"))
    
        return results
    
    def search_tag(self, tag):
        userService = UserProfileService()
        
        results = list() 
        results.append(userService.serialize(userService.search(tag, "istartswith", "username", "first_name", "last_name")))
        
        return results

class CalloutService(BaseService):

    def update_callout_picture(self, callout_id, request):
        callout: Callout = self.get_with_pk(callout_id)
        
        if callout.callout_picture:
            callout.callout_picture.delete(save = False)

        try: 
            callout.callout_picture = request.FILES["callout_picture"]
            callout.save()
            return("Success!")
        except:
            return("Callout not found (probably).")

    def __init__(self):
        super().__init__(Callout, CalloutSerializer)

class UserToCalloutService(BaseService):
    
    def __init__(self):
        super().__init__(Participation, ParticipationSerializer)

    def send_callout_to_user(self, **request_data):
        return self.add_from_request_data(request_data)

    def rollback_callout_to_user(self, **request_data):
        callout = self.get_where(user=request_data["user"], callout=request_data["callout"])
        return self.delete(callout)

    def rollback_callout_global(self, user):
        callout = self.get_where(user=user)
        ok = False
        if callout:
            ok = True

        while callout:
            self.delete(callout)
            callout = self.get_where(user=user)

        if ok:
            return "Success!"
        else: 
            return "Callout not found."

