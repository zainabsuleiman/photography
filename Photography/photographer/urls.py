from django.urls import path
# from accounts.views import RegisterAPI
from .views import UserProfileView
from . import views
urlpatterns = [
    # path('userlist/', views.UserList, name="userlist"),
    path('account/', views.CreateAccount, name="account"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('<str:pk>/details', views.photographerDetails, name="photographerdetails"),
    path('approve/<str:pk>',views.Approve_Photographer, name="approve"),
    path('<str:pk>/activity',views.createActivity,name='create_account'),
    path('activities/<str:pk>/change_status',views.changeActivityStatus,name='change_status'),
    path('<str:pk>/activities/',views.activityList,name='activity_listing'),
    path('<str:pk>/update_profile', views.updateProfile, name="update_profile"),
    path('list',views.photographerList,name='photographer_listing'),
    path('<str:pk>/details/',views.photographerDetails,name='photographer_listing'),
    path('<str:pk>/appointments',views.photographerAppointments,name='photographer_appointments'),
    path('<str:pk>/appointments/half_paid',views.photographerAppointments_half,name='photographer_appointments'),
    path('appointment/<str:pk>/approve',views.approve_appointment,name='photographer_approve_appointment')

]