from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as auth 
from django.contrib.auth import views as auth_views

urlpatterns = [

    # --- USER --- 
    path('get_user_by_id/<int:id>/', views.get_user_by_id),
    path('add_user/', views.add_user),
    path('update_user/', views.update_user),
    path('delete_user/<int:id>/', views.delete_user),

    # --- PROFILE ---
    path('get_user_profile_by_id/<int:id>/', views.get_user_profile_by_id),
    path('update_user_pfp/', views.update_user_profile_picture),
    path('update_user_cover/', views.update_user_cover),
    path('update_user_profile/', views.update_user_profile),
    
    # --- CALLOUT ---
    path('get_callouts/', views.get_callouts),
    path('get_user_callouts/', views.get_user_callouts),
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
    path('delete_user_from_opportunity/<int:id>/', views.delete_user_from_opportunity),

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
    path('send_callout/<int:callout_id>/<int:user_id>/', views.send_callout),

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

    # --- TOKEN ---
    path('get_token/', auth.obtain_auth_token),
    path('get_id/', views.get_id),

    # --- AUTH ---
    path("reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # --- LOGIN ---
    path('register/', views.register),
    path('checkUsername/<str:username>', views.checkUsername),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
