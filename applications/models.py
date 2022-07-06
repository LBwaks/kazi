from django.db import models
from django.db.models.deletion import CASCADE
from jobs.models import Job
from django.contrib.auth.models import User
from  ckeditor.fields import RichTextField
import uuid
from django.urls import reverse
# Create your models here.
class Application(models.Model):
    application_uuid =models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user =models.ForeignKey(User,related_name="user_application",on_delete=models.CASCADE)
    job = models.ForeignKey(Job,related_name="applications", on_delete=models.CASCADE)
    charge=models.IntegerField() 
    other_description = RichTextField(blank=True,null=True)
    status =models.CharField(max_length=100,default='Pending')
    cancel_reject_done_time=models.DateTimeField(blank=True,null=True)
    approved_time = models.DateTimeField(blank=True,null=True)
    # remote_addr = models.GenericIPAddressField(blank=True, null=True, verbose_name=_("remote address"))
    created_at = models.DateTimeField(auto_now_add=True)



    def get_absolute_url(self):
        return reverse('jobs')

class ComplaintsReview(models.Model):
    user = models.ForeignKey(User,related_name='reviews',on_delete=models.CASCADE)
    application  = models.ForeignKey(Application,related_name="applicant_review",on_delete=models.CASCADE)   
    review = RichTextField(blank=True,null=True)
    slug = models.SlugField(max_length=200)
    complaints =RichTextField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        # return reverse("done-page", kwargs={"application_id": self.application_id})
        return reverse("jobs")

    # # application_uuid>/done44444444444',get_done_page,name=''),