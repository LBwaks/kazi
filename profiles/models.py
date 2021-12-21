from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from django.urls import reverse
from PIL import Image

user_type=[
    ('recruiter','Job Recruiter'),
    ('seeker','Job Seeker'),

]
gender =[
    ('male','Male'),
    ('female','Female'),
    ('intersex','Intersex')
]
seeker_taskforce=[
('workshop','I have a workshop'),
('alone','I work alone'),
('other','Other')
]
def user_profile_path(instance, filename):
     return 'users/profile/user_{0}/{1}'.format(instance.user.id, filename)

def user_documents_path(instance, filename):
     return 'users/documents/user_{0}/{1}'.format(instance.user.id, filename)

def user_id_path(instance, filename):
     return 'users/id/user_{0}/{1}'.format(instance.user.id, filename)

# Create your models here.
class Personal(models.Model):
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

    profile_uuid =models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_type =models.CharField(choices=user_type,max_length=30)
    id_passport = models.CharField(unique=True,max_length=14)    
    phone_number = PhoneNumberField()
    gender= models.CharField(choices=gender, max_length=10)
    bio = RichTextField(blank=True,null=True) 
    profile_pic = models.ImageField(upload_to=user_profile_path,blank=True,null=True,default='users/profile/user_0/profile.png')
    county =models.CharField( choices=county_choice, max_length=20,  default=Nairobi)
    location = models.CharField(max_length=250 )
    address = models.CharField(max_length=250)    
    skills = models.CharField(max_length= 100,blank=True,null=True)
    cv = models.FileField(upload_to=user_documents_path,blank=True,null=True)   
    id_front =  models.ImageField(upload_to=user_id_path,blank=True,null=True)
    id_back= models.ImageField(upload_to=user_id_path,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.id_passport

    @property
    def profile_pic_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url

    
    def get_absolute_url(self):
        return reverse("profile", kwargs={"profile_uuid": self.profile_uuid})

def user_documents_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'users/documents/user_{0}/{1}'.format(instance.user.id, filename)

def user_id_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'users/id/user_{0}/{1}'.format(instance.user.id, filename)






    

