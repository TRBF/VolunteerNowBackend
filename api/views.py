from rest_framework.response import Response
from rest_framework.decorators import api_view 
from api.serializers import OrganiserSerializer
from volunteering.services import ExperienceService, EventService, SearchService, VolunteerService, OrganiserService, NotificationService

# ----------- EXPERIENCE ----------

@api_view(['GET'])
def get_experiences(request):
    service = ExperienceService()
    print(service.get_all())
    return Response(service.serialize(service.get_all()))

@api_view(['GET'])
def get_experience_by_id(request, experience_id):
    service = ExperienceService()
    return Response(service.serialize(service.get_with_pk(pk=experience_id)))

@api_view(['GET'])
def get_experience_by_name(request, experience_name):
    service = ExperienceService()
    return Response(service.serialize(service.get_where(name=experience_name)))

@api_view(['POST'])
def add_experience(request):
    service = ExperienceService()
    print(request.data)
    return Response(service.add_from_request_data(request.data))

# ----------- EVENT ----------

@api_view(['GET'])
def get_events(request):
    service = EventService()
    print(service.get_all())
    return Response(service.serialize(service.get_all()))

@api_view(['GET'])
def get_event_by_id(request, event_id):
    service = EventService()
    return Response(service.serialize(service.get_with_pk(pk=event_id)))

@api_view(['GET'])
def get_event_by_name(request, event_name):
    service = EventService()
    return Response(service.serialize(service.get_where(name=event_name)))

@api_view(['POST'])
def add_event(request):
    service = EventService()
    print(request.data)
    return Response(service.add_from_request_data(request.data))

# ----------- VOLUNTEER ----------

@api_view(['GET'])
def get_volunteers(request):
    service = VolunteerService()
    print(service.get_all())
    return Response(service.serialize(service.get_all()))

@api_view(['GET'])
def get_volunteer_by_id(request, volunteer_id):
    service = VolunteerService()
    return Response(service.serialize(service.get_with_pk(pk=volunteer_id)))

@api_view(['GET'])
def get_volunteer_by_name(request, volunteer_name):
    service = VolunteerService()
    return Response(service.serialize(service.get_where(name=volunteer_name)))

@api_view(['POST'])
def add_volunteer(request):
    service = VolunteerService()
    print(request.data)
    return Response(service.add_from_request_data(request.data))

# ----------- ORGANISER ----------

@api_view(['GET'])
def get_organisers(request):
    service = OrganiserService()
    print(service.get_all())
    return Response(service.serialize(service.get_all()))

@api_view(['GET'])
def get_organiser_by_id(request, organiser_id):
    service = OrganiserService()
    return Response(service.serialize(service.get_with_pk(pk=organiser_id)))

@api_view(['GET'])
def get_organiser_by_name(request, organiser_name):
    service = OrganiserService()
    return Response(service.serialize(service.get_where(name=organiser_name)))

@api_view(['POST'])
def add_organiser(request):
    service = OrganiserService()
    print(request.data)
    return Response(service.add_from_request_data(request.data))

# ----------- NOTIFICATION ----------

@api_view(['GET'])
def get_notifications(request):
    service = NotificationService()
    print(service.get_all())
    return Response(service.serialize(service.get_all()))

@api_view(['GET'])
def get_notification_by_id(request, notification_id):
    service = NotificationService()
    return Response(service.serialize(service.get_with_pk(pk=notification_id)))

@api_view(['GET'])
def get_notification_by_name(request, notification_name):
    service = NotificationService()
    return Response(service.serialize(service.get_where(name=notification_name)))

@api_view(['POST'])
def add_notification(request):
    service = NotificationService()
    print(request.data)
    return Response(service.add_from_request_data(request.data))

# ----------- MANY TO MANY ----------

@api_view(['GET'])
def get_volunteers_of_event(request, event_id):
    eventService = EventService()
    volunteerService = VolunteerService()
    return Response(volunteerService.serialize(eventService.get_event_volunteers(event_id)))

@api_view(['GET'])
def get_organisers_of_event(request, event_id):
    eventService = EventService()
    organiserService = OrganiserService()
    return Response(organiserService.serialize(eventService.get_event_organisers(event_id)))

@api_view(['GET'])
def get_events_of_volunteer(request, volunteer_id):
    eventService = EventService()
    volunteerService = VolunteerService()
    return Response(eventService.serialize(volunteerService.get_events_of_volunteer(volunteer_id)))

@api_view(['GET'])
def get_events_of_organiser(request, organiser_id):
    eventService = EventService()
    organiserService = OrganiserService()
    return Response(eventService.serialize(organiserService.get_events_of_organiser(organiser_id)))

@api_view(['POST'])
def add_volunteer_to_event(request):
    service = EventService()
    return Response(service.add_event_volunteer(**request.data))

@api_view(['POST'])
def add_organiser_to_event(request):
    service = EventService()
    return Response(service.add_event_organiser(**request.data))

@api_view(['GET'])
def search(request, query):
    service = SearchService()
    return Response(service.search(query))

@api_view(['GET'])
def search_tag(request, tag):
    service = SearchService()
    return Response(service.search_tag(tag))

@api_view(['GET'])
def get_volunteer_notification(request, volunteer_id):
    volunteerService = VolunteerService()
    notificationService = NotificationService()
    return Response(notificationService.serialize(volunteerService.get_volunteer_notifications(volunteer_id)))

@api_view(['GET'])
def get_volunteer_experiences(request, volunteer_id):
    volunteerService = VolunteerService()
    experienceService = ExperienceService()
    return Response(experienceService.serialize(volunteerService.get_volunteer_experiences(volunteer_id)))

# ---------------------------- OLD ----------------------------
#
# # ----------- EVENT ----------
#
# @api_view(['GET'])
# def get_events(request):
#     events = Event.objects.all() # to be replaced with service
#     serializer = ExperienceSerializer(events, many=True)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def get_event_by_id(request, event_id):
#     print("get_event_by_id - " + str(request))
#     event = Event.objects.get(pk=event_id) # to be replaced with service
#     serializer = EventSerializer(event)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def get_event_by_name(request, event_name):
#     print("get_event_by_name - " + str(request))
#     event = Event.objects.get(name=event_name) # to be replaced with service
#     serializer = EventSerializer(event)
#     return Response(serializer.data)
#
# @api_view(['POST'])
# def add_event(request):
#     print("add_event - " + str(request))
#     serializer = EventSerializer(data=request.data) # to be replaced with service 
#     print(request.data)
#     if serializer.is_valid():
#         serializer.save()
#     print(serializer.errors)
#     return Response(serializer.data)
#
# # ----------- VOLUNTEER ----------
#
# @api_view(['GET'])
# def get_volunteers(request):
#     volunteers = Volunteer.objects.all() # to be replaced with service
#     serializer = VolunteerSerializer(volunteers, many=True)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def get_volunteer_by_id(request, volunteer_id):
#     print("get_volunteer_by_id - " + str(request))
#     volunteer = Volunteer.objects.get(pk=volunteer_id) # to be replaced with service
#     serializer = VolunteerSerializer(volunteer)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def get_volunteer_by_name(request, volunteer_name):
#     print("get_volunteer_by_name - " + str(request))
#     volunteer = Volunteer.objects.get(name=volunteer_name) # to be replaced with service
#     serializer = VolunteerSerializer(volunteer)
#     return Response(serializer.data)
#
# @api_view(['POST'])
# def add_volunteer(request):
#     print("add_volunteer - " + str(request))
#     serializer = VolunteerSerializer(data=request.data) # to be replaced with service 
#     print(request.data)
#     if serializer.is_valid():
#         serializer.save()
#     print(serializer.errors)
#     return Response(serializer.data)
#
# # ----------- ORGANISER ----------
#
# @api_view(['GET'])
# def get_organisers(request):
#     organisers = Organiser.objects.all() # to be replaced with service
#     serializer = OrganiserSerializer(organisers, many=True)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def get_organiser_by_id(request, organiser_id):
#     print("get_organiser_by_id - " + str(request))
#     organiser = Organiser.objects.get(pk=organiser_id) # to be replaced with service
#     serializer = OrganiserSerializer(organiser)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def get_organiser_by_name(request, organiser_name):
#     print("get_organiser_by_name - " + str(request))
#     organiser = Organiser.objects.get(name=organiser_name) # to be replaced with service
#     serializer = OrganiserSerializer(organiser)
#     return Response(serializer.data)
#
# @api_view(['POST'])
# def add_organiser(request):
#     print("add_organiser - " + str(request))
#     serializer = OrganiserSerializer(data=request.data) # to be replaced with service 
#     print(request.data)
#     if serializer.is_valid():
#         serializer.save()
#     print(serializer.errors)
#     return Response(serializer.data)
#
#
# # ----------- NOTIFICATION ----------
#
# @api_view(['GET'])
# def get_notifications(request):
#     notifications = Notification.objects.all() # to be replaced with service
#     serializer = NotificationSerializer(notifications, many=True)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def get_notification_by_id(request, notification_id):
#     print("get_notification_by_id - " + str(request))
#     notification = Notification.objects.get(pk=notification_id) # to be replaced with service
#     serializer = NotificationSerializer(notification)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def get_notification_by_name(request, notification_name):
#     print("get_notification_by_name - " + str(request))
#     notification = Notification.objects.get(name=notification_name) # to be replaced with service
#     serializer = NotificationSerializer(notification)
#     return Response(serializer.data)
#
# @api_view(['POST'])
# def add_notification(request):
#     print("add_notification - " + str(request))
#     serializer = NotificationSerializer(data=request.data) # to be replaced with service 
#     print(request.data)
#     if serializer.is_valid():
#         serializer.save()
#     print(serializer.errors)
#     return Response(serializer.data)
