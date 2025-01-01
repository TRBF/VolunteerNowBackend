from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # --- USERS --- 
    path('get_user_by_id/<int:id>/', views.get_user_by_id),
    path('get_volunteer_by_username/<str:username>/', views.get_user_by_username),
    path('add_user/', views.add_user),
    path('update_user/<int:id>', views.update_user),

    path('update_user_pfp/<int:id>', views.update_user_pfp),
    path('update_user_cover/<int:id>', views.update_user_cover),

    # --- CALLOUTS ---
    path('get_callouts/', views.get_callouts),
    path('get_callout_by_id/<int:id>/', views.get_callout_by_id),
    path('get_callout_sender/<int:id>', views.get_callout_sender),
    path('add_callout/', views.add_callout),
    path('update_callout/<int:id>', views.update_callout),
    path('delete_callout/<int:id>', views.delete_callout),

    path('update_callout_picture/<int:id>', views.update_callout_picture),

    # --- OPPORTUNITY --- 
    path('get_opportunities/', views.get_opportunities),
    path('get_opportunity_by_id/<int:id>/', views.get_opportunity_by_id),
    path('add_opportunity/', views.add_opportunity),
    path('update_opportunity/<int:id>', views.update_opportunity),
    path('delete_opportunity/<int:id>', views.delete_opportunity),

    path('update_opportunity_pfp/<int:id>', views.update_opportunity_pfp),
    path('update_opportunity_cover/<int:id>', views.update_opportunity_cover),
    path('update_opportunity_post_image/<int:id>', views.update_opportunity_post_image),
    path('update_opportunity_post_image/<int:id>', views.update_opportunity_post_image),

    path('add_user_to_opportunity/', views.add_user_to_opportunity),
    path('delete_user_from_opportunity/<int:id>', views.delete_user_from_opportunity),

    # --- PROFILE ---
    path('get_profile/<int:id>', views.get_user_by_id),
    path('edit_profile/<int:id>', views.update_user),

    # -- USER ADDED PARTICIPATIONS --
    path('get_user_added_participations/<int:id>/', views.get_user_added_participations),
    path('add_user_added_participation/', views.add_user_added_participation),
    path('update_user_added_participation/<int:id>/', views.update_user_added_participation),
    path('delete_user_added_participation/<int:id>/', views.delete_user_added_participation),

    path('update_user_added_participation_picture/<int:id>/', views.update_user_added_participation_picture),
    path('update_user_added_participation_diploma/<int:id>/', views.update_user_added_participation_diploma),

    # --- APPLICATIONS ---
    path('get_application/<int:application_id>', views.get_question),
    path('add_application', views.add_application),

    # --- QUESTIONS ---
    path('get_question/<int:question_id>', views.get_question),
    path('add_question', views.add_question),

    # --- PARTICIPATIONS --- 
    path('update_participation/<int:id>', views.update_participation),

    # --- USER TO CALLOUT ---
    path('get_volunteer_callouts/<int:id>', views.get_volunteer_callouts),
    path('get_callout_volunteers/<int:id>', views.get_callout_volunteers),
    path('send_callout/<int:callout_id>/<int:user_id>', views.send_callout),

    # --- RELATIONSHIPS ---
    path('get_opportunity_volunteers/<int:id>', views.get_opportunity_volunteers),
    path('get_opportunity_organisers/<int:id>', views.get_opportunity_organisers),
    path('get_user_opportunities/<int:id>', views.get_user_opportunities),
    path('get_user_participations/<int:id>', views.get_user_participations),
    path('add_user_to_opportunity/', views.add_user_to_opportunity),
    path('add_question_to_application/<int:application_id>', views.add_application_question),
    path('get_application_questions/<int:application_id>', views.get_application_questions),

    # --- GENERALISED --- 
    path('search/<str:query>', views.search),
    path('search_tag/<str:tag>', views.search_tag),
    path('feed/', views.feed),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
