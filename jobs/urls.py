from django.urls import path
from .import views
# from django_filters.views import FilterView
from .views import DeleteJobView, JobDetailView,UserView ,JobView, AddJobView,cancel,done_job,approve_application,UpdateJobView,JobApplicationView,JobApplicationsView,MyJobsView,TagView,pdf,get_done_page

12
urlpatterns = [
    path('',JobView.as_view(), name="jobs"),
    path('my_jobs',MyJobsView.as_view(),name='my_jobs'),
    path('<slug>',JobDetailView.as_view(),name='job_details'),
    path('add_job/',AddJobView.as_view(),name='add_job'),
    path('edit/<slug>',UpdateJobView.as_view(),name="update_job"),
    path('delete/<slug>',DeleteJobView.as_view(),name="delete_job"),
    path('this_job_applications/<slug>',JobApplicationsView.as_view(),name="this_job_applications"),
    path('<application_uuid>/approvekkkkkkkkk',approve_application,name="approve"),
    path('<application_uuid>/donegggggggggg',done_job,name='done'),
    path('<application_uuid>/done44444444444',get_done_page,name='done-page'),
    path('<application_uuid>/cancel',cancel,name='cancel_job'),
    path('tags/<slug>/',TagView,name="tags"),
    path('jobs_by/<username>/',UserView,name="jobs_by"),
    # path('LLLL/pdfhhhj',get_invoice,name="pdf"),
    path('<application_uuid>/ppp/pdf',pdf,name="get-invoice"),
    # path('search/',views.search,name='search'),  
    # path('applicant/<slug>/applicant',ApplicantProfileView.as_view(),name="applicant"),

    # path('<slug>/applications',JobApplicationView.as_view(),name="job_applications")
    # path('this_job_applications/<slug>/approve', ApproveApplication.as_view(),name="approve"),
    # path('my_jobs/<str:username>',MyJobsView.as_view(),name='my_jobs'),
    # path('my_jobs',MyJobsView.as_view(),name='my_jobs'),

]
