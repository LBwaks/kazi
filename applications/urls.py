from django.urls import path 
from .views import ApplicationView,MyApplicationsView,AddApplicationView,JobApplicationsView,application_done_job,ApplicantProfileView,AddReviewComplaintView,cancel_application, reject_job
# ,approve_application
# ,ApplicationDetailView
# from applications.views import MyApplicationView

urlpatterns = [
    path('',ApplicationView.as_view(),name='applications'),
    # path('<profile_uuid>',ApplicationDetailView.as_view(),name='application-details'),
    path('apply_job/<job_id>/',AddApplicationView.as_view(),name="apply_job"),
    # path('review/<application_id>/',AddReviewComplaintView.as_view(),name="review_complaint"),
    path('job_applications', MyApplicationsView.as_view(),name="my_application"),
    path('applicant/<username>/',ApplicantProfileView,name="applicant"),
    path('<application_uuid>/cancel',cancel_application,name='cancel_application'),
    path('<application_uuid>/reject',reject_job,name='reject_job_approval'),
    path('<application_uuid>/donenooooooooooooooooo',application_done_job,name='done_job'),
    # path('<application_uuid>/donerrrrrrrrrrr', done_job,name='done')
    # path('<application_uuid>/approve',approve_application,name="approve"),
    # path('this_job_applications/<job_slug>',JobApplicationsView.as_view(),name="this_job_applications")

]
