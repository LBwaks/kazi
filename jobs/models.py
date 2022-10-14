from msilib.schema import LockPermissions
from turtle import title
from django.db import models
from autoslug import AutoSlugField
from django.conf import settings
from  ckeditor.fields import RichTextField
from django.db.models.deletion import CASCADE
from django.urls import reverse
import uuid,datetime
from PIL import Image
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.postgres.indexes import GinIndex
from pkg_resources import to_filename
from django.template.defaultfilters import slugify
from prompt_toolkit import application
import random,string

class Category(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,editable=False,on_delete=models.CASCADE,null=False)
    name = models.CharField(max_length = 255)
    slug = AutoSlugField(populate_from='name', unique=True)
    description =RichTextField()
    created_date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("tags",kwargs={'slug':self.slug})

    def save(self,*args, **kwargs):
        self.slug= slugify(self.name)
        return super(Category,self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("artist_category",kwargs={'slug':self.slug})

class Tag(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,editable=False,on_delete=models.CASCADE,null=False,related_name='job_tag_user')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='blog_category_tag')  
    name = models.CharField(max_length = 255)
    slug = AutoSlugField(populate_from='name', unique=True)
    description =RichTextField()
    created_date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("tags",kwargs={'slug':self.slug})
    def save(self,*args, **kwargs):
        self.slug= slugify(self.name)
        return super(Tag,self).save(*args, **kwargs)

def random_string_generator(size=10,chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_job_id_generator(instance):
    
    new_job_id =random_string_generator().upper()
    Klass = instance.__class__
    qs_exists =Klass.objects.filter(job_id =new_job_id).exists()
    if qs_exists:
        return unique_job_id_generator(instance)
    return new_job_id

# Create your models here.
class Job(models.Model):
    Mombasa = 'Mombasa'
    Kwale= 'Kwale'
    Kilifi= 'Kilifi'
    TanaRiver= 'Tana River'
    Lamu= 'Lamu'
    TaitaTaveta= 'Taita-Taveta'
    Garissa ='Garissa'
    Wajir= 'Wajir'
    Mandera= 'Mandera'
    Marsabit= 'Marsabit'
    Isiolo= 'Isiolo'
    MERU= 'MERU'
    TharakaNithi= 'Tharaka-Nithi'
    Embu= 'Embu'
    Kitui ='Kitui'
    Machakos= 'Machakos'
    Makueni= 'Makueni'
    Nyandarua= 'Nyandarua'
    Nyeri= 'Nyeri'
    Kirinyaga='Kirinyaga'
    Muranga="Muranga"
    Kiambu= 'Kiambu'
    Turkana ='Turkana'
    WestPokot='West Pokot'
    Samburu= 'Samburu'
    TransNzoia ='Trans Nzoia'
    UasinGishu= 'Uasin Gishu'
    ElgeyoMarakwet= 'Elgeyo-Marakwet'
    Nandi ='Nandi'
    Baringo= 'Baringo'
    Laikipia ='Laikipia'
    Nakuru= 'Nakuru'
    Narok= 'Narok'
    Kajiado= 'Kajiado'
    Kericho= 'Kericho'
    Bomet= 'Bomet'
    Kakamega ='Kakamega'
    Vihiga= 'Vihiga'
    Bungoma= 'Bungoma'
    Busia= 'Busia'
    Siaya= 'Siaya'
    Kisumu ='Kisumu'
    HomaBay= 'Homa Bay'
    Migori= 'Migori'
    Kisii= 'Kisii'
    Nyamira= 'Nyamira'
    Nairobi= 'Nairobi'

    county_choice= [
        (Mombasa, 'Mombasa'),
        (Kwale, 'Kwale'),
        (Kilifi, 'Kilifi'),
        (TanaRiver, 'Tana River'),
        (Lamu, 'Lamu'),
        (TaitaTaveta, 'Taita-Taveta'),
        (Garissa ,'Garissa'),
        (Wajir, 'Wajir'),
        (Mandera, 'Mandera'),
        (Marsabit, 'Marsabit'),
        (Isiolo, 'Isiolo'),
        (MERU, 'Meru'),
        (TharakaNithi, 'Tharaka-Nithi'),
        (Embu, 'Embu'),
        (Kitui ,'Kitui'),
        (Machakos, 'Machakos'),
        (Makueni, 'Makueni'),
        (Nyandarua, 'Nyandarua'),
        (Nyeri, 'Nyeri'),
        (Kirinyaga,'Kirinyaga'),
        (Muranga,"Murang'a"),
        (Kiambu, 'Kiambu'),
        (Turkana ,'Turkana'),
        (WestPokot,' West Pokot'),
        (Samburu, 'Samburu'),
        (TransNzoia ,'Trans Nzoia'),
        (UasinGishu, 'Uasin Gishu'),
        (ElgeyoMarakwet, 'Elgeyo-Marakwet'),
        (Nandi ,'Nandi'),
        (Baringo, 'Baringo'),
        (Laikipia ,'Laikipia'),
        (Nakuru, 'Nakuru'),
        (Narok, 'Narok'),
        (Kajiado, 'Kajiado'),
        (Kericho, 'Kericho'),
        (Bomet, 'Bomet'),
        (Kakamega ,'Kakamega'),
        (Vihiga, 'Vihiga'),
        (Bungoma, 'Bungoma'),
        (Busia, 'Busia'),
        (Siaya, 'Siaya'),
        (Kisumu ,'Kisumu'),
        (HomaBay, 'Homa Bay'),
        (Migori, 'Migori'),
        (Kisii, 'Kisii'),
        (Nyamira, 'Nyamira'),
        (Nairobi, 'Nairobi'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=False)
    job_id = models.CharField(blank=True,max_length=30)
    title = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='title', unique=True)
    tag = models.ForeignKey(Tag,verbose_name="Tag",on_delete=models.CASCADE)
    description = RichTextField()
    application_deadline = models.DateTimeField(auto_now_add=False)
    job_done_date = models.DateTimeField(auto_now_add=False)
    county =models.CharField( choices=county_choice, max_length=20,  default=Nairobi)
    location= models.CharField(max_length=250)
    address = models.CharField(max_length=250)   
    status = models.CharField(max_length=250,blank=True,null=True,default="waiting")
    is_featured = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    image =models.ImageField(upload_to='jobs/job_images/',default='jobs/job_images/jobs.jpg',blank=True,null=True)
    video =models.FileField(upload_to='jobs/job_videos/',blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)



    class Meta:
        indexes = [
            GinIndex(name='NewGinIndex',fields=['title',],opclasses=['gin_trgm_ops'])
            ]
 
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("job_details", kwargs={"slug": self.slug})
        
    def get_related_job_by_tag(self):
        return Job.objects.filter(application_deadline__gte=datetime.datetime.now(),status='waiting',tag_id =self.tag_id).exclude(pk=self.pk).order_by('-created_date')[:8]
   
    @property 
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url 
    def save(self,*args, **kwargs):
        self.slug= slugify(self.title)
        return super(Job,self).save(*args, **kwargs)
    @property 
    def video_url(self):
        if self.video and hasattr(self.video, 'url'):
            return self.video.url 

def pre_save_job_id(sender,instance,*args,**kwargs):
        if not instance.job_id:
            instance.job_id = unique_job_id_generator(instance)
pre_save.connect(pre_save_job_id,sender=Job)


   
    
class JobImage(models.Model):
    job =models.ForeignKey(Job,on_delete=models.CASCADE)
    image =models.ImageField(upload_to='jobs/job_images/',default='jobs/job_images/jobs.jpg',blank=True,null=True)

    @property 
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url 
            
    # def __str__(self) -> str:
    #     return super(self.job.title + 'image').__str__()

    

# class Invoice(models.Model):
#     invoice id
#     invoice date
#     invoice due
#     invoice status
#     invoice to_
#     invoice job title
#     invoice application charge