from rest_framework.response import Response
from rest_framework.decorators import api_view 
from api.serializers import UserSerializer
from volunteering import services
from volunteering.models import Participation
from volunteering.services import OpportunityService, ParticipationService, QuestionService, SearchService, UserService, CalloutService, UserAddedParticipationService, ApplicationService, UserToCalloutService



# ----------- OPPORTUNITY ----------

@api_view(['GET'])
def get_opportunities(request):
    service = OpportunityService()
    print(service.get_all())
    return Response(service.serialize(service.get_all()))

@api_view(['DELETE'])
def delete_opportunity(request, id):
    service = OpportunityService()
    return Response(service.serialize(service.delete_with_pk(pk=id)))

@api_view(['GET'])
def get_opportunity_by_id(request, id):
    service = OpportunityService()
    return Response(service.serialize(service.get_with_pk(pk=id)))

@api_view(['GET'])
def get_opportunity_by_name(request, opportunity_name):
    service = OpportunityService()
    return Response(service.serialize(service.get_where(name=opportunity_name)))

@api_view(['POST'])
def add_opportunity(request):
    service = OpportunityService()
    print(request.data)
    return Response(service.add_from_request_data(request.data))

@api_view(['PUT'])
def update_opportunity(request, id):
    service = OpportunityService()
    response = Response(service.update(id, request.data))
    return response

@api_view(['PUT'])
def update_opportunity_pfp(request, id):
    service = OpportunityService()
    if(request.FILES.get("profile_picture")):
        return Response(service.update_opportunity_pfp(id, request))
    else:
        return Response("update_pfp() was called without a profile picture.")

@api_view(['PUT'])
def update_opportunity_cover(request, id):
    service = OpportunityService()
    if(request.FILES["cover_image"]):
        return Response(service.update_opportunity_cover(id, request))
    else:
        return Response("update_opportunity_cover() was called without a cover image.")

@api_view(['PUT'])
def update_opportunity_post_image(request, id):
    service = OpportunityService()
    if(request.FILES.get("post_image")):
        return Response(service.update_opportunity_post_image(id, request))
    else:
        return Response("update_user_cover() was called without a cover image.")



# ----------- USER ----------

@api_view(['GET'])
def get_user_by_id(request, id):
    service = UserService()
    return Response(service.serialize(service.get_with_pk(id)))

@api_view(['GET'])
def get_user_by_username(request, username):
    service = UserService()
    return Response(service.serialize(service.get_where(username=username)))

@api_view(['POST'])
def add_user(request):
    service = UserService()
    response = Response(service.add_from_request_data(request.data)) 
    return response

@api_view(['PUT'])
def update_user(request, id):
    service = UserService()
    response = Response(service.update(id, request.data))
    return response

@api_view(['PUT'])
def update_user_pfp(request, id):
    service = UserService()
    if(request.FILES.get("profile_picture")):
        return Response(service.update_user_pfp(id, request))
    else:
        return Response("update_pfp() was called without a profile picture.")

@api_view(['PUT'])
def update_user_cover(request, id):
    service = UserService()
    if(request.FILES.get("cover_image")):
        return Response(service.update_user_cover(id, request))
    else:
        return Response("update_user_cover() was called without a cover image.")

@api_view(['DELETE'])
def delete_user(request, id):
    service = UserService()
    return Response(service.serialize(service.delete_with_pk(pk=id)))



# ----------- CALLOUTS ----------

@api_view(['GET'])
def get_callouts(request):
    service = CalloutService()
    print(service.get_all())
    return Response(service.serialize(service.get_all()))

@api_view(['GET'])
def get_callout_by_id(request, id):
    service = CalloutService()
    return Response(service.serialize(service.get_with_pk(pk=id)))

@api_view(['GET'])
def get_callout_sender(request, id):
    calloutService = CalloutService()
    userService = UserService()
    callout = calloutService.get_with_pk(id)
    return Response(userService.serialize(callout.sender))

@api_view(['POST'])
def add_callout(request):
    service = CalloutService()
    print(request.data)
    return Response(service.add_from_request_data(request.data))

@api_view(['PUT'])
def update_callout(request, id):
    service = CalloutService()
    response = Response(service.update(id, request.data))
    return response

@api_view(['DELETE'])
def delete_callout(request, id):
    service = CalloutService()
    response = Response(service.delete_with_pk(pk=id))
    return response

@api_view(['PUT'])
def update_callout_picture(request, id):
    service = CalloutService()
    if(request.FILES.get("callout_picture")):
        return Response(service.update_callout_picture(id, request))
    else:
        return Response("update_callout_picture() was called without a profile picture.")


# ----------- USER TO CALLOUT ----------


@api_view(['GET'])
def get_volunteer_callouts(request, id):
    utc_service = UserToCalloutService()
    callout_service = CalloutService()
    return Response(callout_service.serialize(utc_service.get_where(user=id)))
 
@api_view(['GET'])
def get_callout_volunteers(request, id):
    utc_service = UserToCalloutService()
    user_service = UserService()
    return Response(user_service.serialize(utc_service.get_where(callout=id)))
    
@api_view(['POST'])
def send_callout(request, callout_id, user_id):
    service = UserToCalloutService()
    return Response(service.send_callout_to_user(callout=callout_id, user=user_id))

# ----------- USER ADDED PARTICIPATION ---------- 


@api_view(['GET'])
def get_user_added_participations(request, id):
    service = UserAddedParticipationService()
    print("\n\n\nuser id:", service.serialize(service.get_where(user=id)))
    return Response(service.serialize(service.get_where(user=id)))

@api_view(['POST'])
def add_user_added_participation(request):
    service = UserAddedParticipationService()
    return Response(service.add_from_request_data(request.data))

@api_view(['PUT'])
def update_user_added_participation(request, id):
    service = UserAddedParticipationService()
    response = Response(service.update(id, request.data))
    return response

@api_view(['DELETE'])
def delete_user_added_participation(request, id):
    service = UserAddedParticipationService()
    response = Response(service.delete_with_pk(pk=id))
    return response

@api_view(['PUT'])
def update_user_added_participation_picture(request, id):
    service = UserAddedParticipationService()
    if(request.FILES.get("participation_picture")):
        return Response(service.update_participation_picture(id, request))
    else:
        return Response("update_participation_picture() was called without a profile picture.")

@api_view(['PUT'])
def update_user_added_participation_diploma(request, id):
    service = UserAddedParticipationService()
    if(request.FILES.get("diploma")):
        return Response(service.update_participation_diploma(id, request))
    else:
        return Response("update_participation_diploma() was called without a profile picture.")



# ----------- QUESTION -----------

@api_view(['GET'])
def get_question(request, id):
    service = QuestionService()
    response = Response(service.get_with_pk(pk=id))
    return response

@api_view(['POST'])
def add_question(request, id):
    service = QuestionService()
    response = Response(service.add_from_request_data(request.data)) 
    return response

@api_view(['PUT'])
def update_question(request, id):
    service = QuestionService()
    response = Response(service.update(id, request.data)) 
    return response

@api_view(['DELETE'])
def delete_question(request, id):
    service = QuestionService()
    response = Response(service.delete_with_pk(id)) 
    return response

# ----------- APPLICATION -----------

@api_view(['GET'])
def get_application(request, id):
    service = ApplicationService()
    response = Response(service.get_with_pk(pk=id))
    return response

@api_view(['POST'])
def add_application(request, id):
    service = ApplicationService()
    response = Response(service.add_from_request_data(request.data)) 
    return response

@api_view(['PUT'])
def update_application(request, id):
    service = ApplicationService()
    response = Response(service.update(id, request.data)) 
    return response

@api_view(['DELETE'])
def delete_application(request, id):
    service = ApplicationService()
    response = Response(service.delete_with_pk(id)) 
    return response





# ----------- MANY TO MANY ----------

@api_view(['GET'])
def get_opportunity_volunteers(request, id):
    opportunityService = OpportunityService()
    userService = UserService()
    return Response(userService.serialize(opportunityService.get_opportunity_volunteers(id)))

@api_view(['GET'])
def get_opportunity_organisers(request, id):
    opportunityService = OpportunityService()
    userService = UserService()
    return Response(userService.serialize(opportunityService.get_opportunity_organisers(id)))

@api_view(['GET'])
def get_user_opportunities(request, id):
    opportunityService = OpportunityService()
    userService = UserService()
    return Response(opportunityService.serialize(userService.get_user_opportunities(id)))

@api_view(['GET'])
def get_user_participations(request, id):
    service = ParticipationService()
    return Response(service.serialize(service.get_user_participations(id)))

@api_view(['POST'])
def add_user_to_opportunity(request):
    service = ParticipationService()
    return Response(service.add_participation(**request.data))

@api_view(['GET'])
def search(request, query):
    service = SearchService()
    return Response(service.search(query))

@api_view(['GET'])
def search_tag(request, tag):
    service = SearchService()
    return Response(service.search_tag(tag))

@api_view(['PUT'])
def update_participation(request, id):
    service = ParticipationService()
    response = Response(service.update(id, request.data))
    return response

@api_view(['GET'])
def feed(request):
    service = OpportunityService()
    response = Response(service.get_all())
    return response

@api_view(['DELETE'])
def delete_user_from_opportunity(request, id):
    service  = ParticipationService()
    return Response(service.serialize(service.delete_with_pk(pk=id)))

@api_view(['PUT'])
def add_question_to_application(request, id):
    return Response("Not yet implemented.")

@api_view(['GET'])
def get_application_questions(request, id):
    return Response("Not yet implemented.")

@api_view(['PUT'])
def add_application_question(request, id):
    return Response("Not yet implemented.")

