from django.urls import path
from . import views

urlpatterns = [
    # --- EXPERIENCES--- 
    path('get_experiences/', views.get_experiences),
    path('get_experience_by_id/<int:experience_id>/', views.get_experience_by_id),
    path('get_experience_by_name/<str:experience_name>/', views.get_experience_by_name),
    path('add_experience/', views.add_experience),

    # --- EVENTS --- 
    path('get_events/', views.get_events),
    path('get_event_by_id/<int:event_id>/', views.get_event_by_id),
    path('get_event_by_name/<str:event_name>/', views.get_event_by_name),
    path('add_event/', views.add_event),

    # --- VOLUNTEERS --- 
    path('get_volunteers/', views.get_volunteers),
    path('get_volunteer_by_id/<int:volunteer_id>/', views.get_volunteer_by_id),
    path('get_volunteer_by_name/<str:volunteer_name>/', views.get_volunteer_by_name),
    path('add_volunteer/', views.add_volunteer),

    # --- ORGANISERS ---
    path('get_organisers/', views.get_organisers),
    path('get_organiser_by_id/<int:organiser_id>/', views.get_organiser_by_id),
    path('get_organiser_by_name/<str:organiser_name>/', views.get_organiser_by_name),
    path('add_organiser/', views.add_organiser),

    # --- NOTIFICATIONS ---
    path('get_notifications/', views.get_notifications),
    path('get_notification_by_id/<int:notification_id>/', views.get_notification_by_id),
    path('get_notification_by_name/<str:notification_name>/', views.get_notification_by_name),
    path('add_notification/', views.add_notification),

    # --- MANY TO MANY ---
    path('get_volunteers_of_event/<int:event_id>', views.get_volunteers_of_event),
    path('get_organisers_of_event/<int:event_id>', views.get_organisers_of_event),
    path('get_events_of_volunteer/<int:volunteer_id>', views.get_events_of_volunteer),
    path('get_events_of_organiser/<int:organiser_id>', views.get_events_of_organiser),
    path('add_volunteer_to_event/', views.add_volunteer_to_event),
    path('add_organiser_to_event/', views.add_organiser_to_event),
]
