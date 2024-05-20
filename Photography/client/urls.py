from django.urls import path
# from accounts.views import RegisterAPI
from . import views
from .views import UserProfileView

urlpatterns = [
    # path('userlist/', views.UserList, name="userlist"),
    path('account/', views.CreateAccount, name="account"),
    path('profile/', UserProfileView.as_view(), name='profile'),#userprofile
    path('<str:pk>/make_appointment/',views.createAppointment,name="createappointment"),
    path('appointment/<str:pk>/appointment_details',views.appointmentDetails,name="appointment details"),
    path('<str:pk>/details/',views.Clientdetails,name="details"),
    path('list/',views.listofClient,name="list"),  
    path('Userslist/',views.Userslist,name="Userslist"), #users List
    path('appointment/<str:pk>/assign_activity',views.assignAppointmentActivity,name='assign_appointment_activity'),
    path('<str:pk>/appointments',views.listClientAppointments,name='list_clients_appointment'),
    path('appointment',views.ClientAppointments,name='list_clients_appointment'),
    path('<str:pk>/approved',views.listClientAppointments_approved,name='list_clients_appointment'),
    path('<str:pk>/payment',views.CreatePlan,name='list_clients_appointment'),
    path('appointment/<str:pk>/upload/files', views.FilesUploadAPIView.as_view()),
    path('appointment/<str:pk>/upload', views.Uploads, name='uploads'),

    

]