from http.client import ResponseNotReady
from operator import call
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes 
from volunteering.models import UserProfile
from volunteering.services import OpportunityService, ParticipationService, QuestionService, SearchService, UserProfileService, CalloutService, UserAddedParticipationService, ApplicationService, UserService, UserToCalloutService
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication 

# ----------- OPPORTUNITY ----------

@api_view(['GET'])
def get_opportunities(request):
    service = OpportunityService()
    return Response(service.serialize(service.get_all()))

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_opportunity(request, id):
    if(request.user.is_superuser):
        service = OpportunityService()
        return Response(service.serialize(service.delete_with_pk(pk=id)))
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['GET'])
def get_opportunity_by_id(request, id):
    service = OpportunityService()
    return Response(service.serialize(service.get_with_pk(pk=id)))

@api_view(['GET'])
def get_opportunity_by_name(request, opportunity_name):
    service = OpportunityService()
    return Response(service.serialize(service.get_where(name=opportunity_name)))

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_opportunity(request):
    if(request.user.is_superuser):
        service = OpportunityService()
        return Response(service.add_from_request_data(request.data))
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_opportunity(request, id):
    if(request.user.is_superuser):
        service = OpportunityService()
        response = Response(service.update(id, request.data))
        return response
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_opportunity_pfp(request, id):
    if(request.user.is_superuser):
        service = OpportunityService()
        if(request.FILES.get("profile_picture")):
            return Response(service.update_opportunity_pfp(id, request))
        else:
            return Response("update_pfp() was called without a profile picture.")
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_opportunity_cover(request, id):
    if(request.user.is_superuser):
        service = OpportunityService()
        if(request.FILES["cover_image"]):
            return Response(service.update_opportunity_cover(id, request))
        else:
            return Response("update_opportunity_cover() was called without a cover image.")
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_opportunity_post_image(request, id):
    if(request.user.is_superuser):
        service = OpportunityService()
        if(request.FILES.get("post_image")):
            return Response(service.update_opportunity_post_image(id, request))
        else:
            return Response("update_user_cover() was called without a cover image.")
    else:
        return Response("Request denied. Insufficient permissions.")



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
    userService = UserService()
    if(request.user.is_superuser):
        return Response(userService.add_from_request_data(request.data))
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    service = UserService()
    response = Response(service.update(request.user.id, request.data))
    return response

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, id):
    service = UserService()
    return Response(service.serialize(service.delete_with_pk(pk=request.user.id)))

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_id(request):
    return Response({"id": request.user.id})

# ----------- USER PROFILE ----------

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user_profile_picture(request):
    userService = UserService()
    userProfileService = UserProfileService()
    user = userService.get_with_pk(request.user.id)
    print(request.data["profile_picture"])
    if(request.data["profile_picture"]):
        return Response(userProfileService.update_user_pfp(user.profile.id, request))
    else:
        return Response("update_pfp() was called without a profile picture.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user_cover(request):
    userService = UserService()
    userProfileService = UserProfileService()
    user = userService.get_with_pk(request.user.id)
    if(request.FILES.get("cover_image")):
        return Response(userProfileService.update_user_cover(user.profile.id, request))
    else:
        return Response("update_user_cover() was called without a cover image.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    userService = UserService()
    userProfileService = UserProfileService()
    user = userService.get_with_pk(request.user.id)
    response = Response(userProfileService.update(user.profile.id, request.data))
    return response

@api_view(['GET'])
def get_user_profile_by_id(request, id):
    userService = UserService()
    userProfileService = UserProfileService()
    user = userService.get_with_pk(id)
    response = userProfileService.serialize(user.profile)
    hours = userProfileService.get_user_hours(id)
    most_fq = userProfileService.get_user_most_fq(id)
    count = userProfileService.get_user_participations_count(id)
    response.update({"first_name": user.first_name, "last_name": user.last_name, "username": user.username, "hours": hours, "most_fq": most_fq, "count": count})
    return Response(response)

# ----------- CALLOUTS ----------

@api_view(['GET'])
def get_callouts(request):
    service = CalloutService()
    return Response(service.serialize(service.get_all()))

@api_view(['GET'])
def get_callout_by_id(request, id):
    service = CalloutService()
    return Response(service.serialize(service.get_with_pk(pk=id)))

@api_view(['GET'])
def get_callout_sender(request, id):
    calloutService = CalloutService()
    userService = UserProfileService()
    callout = calloutService.get_with_pk(id)
    return Response(userService.serialize(callout.sender))

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_callouts(request):
    utc_service = UserToCalloutService()
    callout_service = CalloutService()
    uTCs = utc_service.get_where(user=request.user.id)
    response = []
    for uTC in uTCs:
        callout = callout_service.serialize(uTC.callout)
        callout["time"] = uTC.time
        response.append(callout)
    return Response(response)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_callout(request):
    if(request.user.is_superuser):
        service = CalloutService()
        return Response(service.add_from_request_data(request.data))
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_callout(request, id):
    if(request.user.is_superuser):
        service = CalloutService()
        response = Response(service.update(id, request.data))
        return response
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_callout(request, id):
    if(request.user.is_superuser):
        service = CalloutService()
        response = Response(service.delete_with_pk(pk=id))
        return response
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_callout_picture(request, id):
    if(request.user.is_superuser):
        service = CalloutService()
        if(request.FILES.get("callout_picture")):
            return Response(service.update_callout_picture(id, request))
        else:
            return Response("update_callout_picture() was called without a profile picture.")
    else:
        return Response("Request denied. Insufficient permissions.")


# ----------- USER TO CALLOUT ----------


@api_view(['GET'])
def get_volunteer_callouts(request, id):
    utc_service = UserToCalloutService()
    callout_service = CalloutService()
    return Response(callout_service.serialize(utc_service.get_where(user=id)))
 
@api_view(['GET'])
def get_callout_volunteers(request, id):
    utc_service = UserToCalloutService()
    user_service = UserProfileService()
    return Response(user_service.serialize(utc_service.get_where(callout=id)))
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_callout(request, callout_id, user_id):
    if(request.user.is_superuser):
        service = UserToCalloutService()
        return Response(service.send_callout_to_user(callout=callout_id, user=user_id))
    else:
        return Response("Request denied. Insufficient permissions.")

# ----------- USER ADDED PARTICIPATION ---------- 


@api_view(['GET'])
def get_user_added_participations(request, id):
    service = UserAddedParticipationService()
    return Response(service.serialize(service.get_where(user=id)))

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_user_added_participation(request):
    service = UserAddedParticipationService()
    request.data.update({"user": request.user.id})
    return Response(service.add_from_request_data(request.data))

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user_added_participation(request, id):
    service = UserAddedParticipationService()
    if(request.user.id == service.get_with_pk(id).user_id):
        service = UserAddedParticipationService()
        response = Response(service.update(id, request.data))
        return response
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user_added_participation(request, id):
    service = UserAddedParticipationService()
    if(request.user.id == service.get_with_pk(id).user_id):
        service = UserAddedParticipationService()
        response = Response(service.delete_with_pk(pk=id))
        return response
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user_added_participation_picture(request, id):
    service = UserAddedParticipationService()
    if(request.user.id == service.get_with_pk(id).user_id):
        service = UserAddedParticipationService()
        if(request.FILES.get("user_added_participation_picture")):
            return Response(service.update_participation_picture(id, request))
        else:
            return Response("update_participation_picture() was called without a profile picture.")
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user_added_participation_diploma(request, id):
    service = UserAddedParticipationService()
    if(request.user.id == service.get_with_pk(id).user_id):
        service = UserAddedParticipationService()
        if(request.FILES.get("diploma")):
            return Response(service.update_participation_diploma(id, request))
        else:
            return Response("update_participation_diploma() was called without a diploma.")
    else:
        return Response("Request denied. Insufficient permissions.")

# ----------- QUESTION -----------

@api_view(['GET'])
def get_question(request, id):
    service = QuestionService()
    response = Response(service.get_with_pk(pk=id))
    return response

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_question(request):
    if(request.user.is_superuser):
        service = QuestionService()
        response = Response(service.add_from_request_data(request.data)) 
        return response
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_question(request, id):
    if(request.user.is_superuser):
        service = QuestionService()
        response = Response(service.update(id, request.data)) 
        return response
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_question(request, id):
    if(request.user.is_superuser):
        service = QuestionService()
        response = Response(service.delete_with_pk(id)) 
        return response
    else:
        return Response("Request denied. Insufficient permissions.")

# ----------- APPLICATION -----------

@api_view(['GET'])
def get_application(request, id):
    service = ApplicationService()
    response = Response(service.get_with_pk(pk=id))
    return response

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_application(request):
    if(request.user.is_superuser):
        service = ApplicationService()
        response = Response(service.add_from_request_data(request.data)) 
        return response
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_application(request, id):
    if(request.user.is_superuser):
        service = ApplicationService()
        response = Response(service.update(id, request.data)) 
        return response
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_application(request, id):
    if(request.user.is_superuser):
        service = ApplicationService()
        response = Response(service.delete_with_pk(id)) 
        return response
    else:
        return Response("Request denied. Insufficient permissions.")



# ----------- MANY TO MANY ----------

@api_view(['GET'])
def get_opportunity_volunteers(request, id):
    opportunityService = OpportunityService()
    userService = UserProfileService()
    return Response(userService.serialize(opportunityService.get_opportunity_volunteers(id)))

@api_view(['GET'])
def get_opportunity_organisers(request, id):
    opportunityService = OpportunityService()
    userService = UserProfileService()
    return Response(userService.serialize(opportunityService.get_opportunity_organisers(id)))

@api_view(['GET'])
def get_user_opportunities(request, id):
    opportunityService = OpportunityService()
    userService = UserProfileService()
    return Response(opportunityService.serialize(userService.get_user_opportunities(id)))

@api_view(['GET'])
def get_user_participations(request, id):
    service = ParticipationService()
    return Response(service.serialize(service.get_user_participations(id)))

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_user_to_opportunity(request):
    if(request.user.is_superuser):
        service = ParticipationService()
        return Response(service.add_participation(**request.data))
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['GET'])
def search(request, query):
    service = SearchService()
    return Response(service.search(query))

@api_view(['GET'])
def search_tag(request, tag):
    service = SearchService()
    return Response(service.search_tag(tag))

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_participation(request, id):
    if(request.user.is_superuser):
        service = ParticipationService()
        response = Response(service.update(id, request.data))
        return response
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def feed(request):
    service = OpportunityService()
    response = Response(service.get_all())
    # this should be replaced with something that generates an actual feed
    return response

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user_from_opportunity(request, id):
    if(request.user.is_superuser):
        service  = ParticipationService()
        return Response(service.serialize(service.delete_with_pk(pk=id)))
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_question_to_application(request, id):
    if(request.user.is_superuser):
        return Response("Not yet implemented.")
    else:
        return Response("Request denied. Insufficient permissions.")

@api_view(['GET'])
def get_application_questions(request, id):
    return Response("Not yet implemented.")

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_application_question(request, id):
    if(request.user.is_superuser):
        return Response("Not yet implemented.")
    else:
        return Response("Request denied. Insufficient permissions.")



# ----------- REGISTER ----------

@api_view(['POST'])
def register(request):
    service = UserService()
    return Response(service.add_from_request_data(request.data))

@api_view(['GET'])
def checkUsername(request, username):
    service = UserService()
    return Response(service.serialize(service.get_where(username=username)))

