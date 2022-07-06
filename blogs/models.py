from statistics import mode
from django.db import models
from ckeditor.fields import RichTextField
import datetime
from django.utils import timezone
from autoslug import AutoSlugField
from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify  

class Tag(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,editable=False,on_delete=models.CASCADE,null=False,related_name='blog_tag_user')
    name = models.CharField(max_length = 255)
    slug = AutoSlugField(populate_from='name', unique=True)
    description =RichTextField()
    created_date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.name
    def save(self,*args, **kwargs):
        self.slug= slugify(self.name)
        return super(Tag,self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("blog_tags",kwargs={'slug':self.slug})



class Blog(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,editable=False,on_delete=models.CASCADE,null=False)
    title = models.CharField(max_length = 255)
    slug = AutoSlugField(populate_from='title', unique=True)
    # category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='blog_category')  
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE,related_name='blog_tag')     
    description = RichTextField()
    photo= models.ImageField(upload_to ='blogs/blog_images/',default='blogs/blog_images/blogs.png')
    
    # is_cancelled = models.BooleanField(default=False)
    likes =models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='Blog_likes',blank=True)
  
    created_date = models.DateTimeField(auto_now_add=True)




    def __str__(self):
        return self.title
    def save(self,*args, **kwargs):
        self.slug= slugify(self.title)
        return super(Blog,self).save(*args, **kwargs)
    def total_likes(self):
        return self.likes.count()
    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})
    
    def get_related_blogs_by_tags(self):
        return Blog.objects.filter(tag_id=self.tag_id).exclude(pk=self.pk)
    

class Blog_Comment(models.Model):
    blog=models.ForeignKey(Blog, related_name="blog_comments",on_delete=models.CASCADE,null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # likes =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,related_name='comments_likes')
    # reply = models.ForeignKey('Blog_Comment', null=True, related_name='blog_replies', blank=True, on_delete=models.CASCADE)
    parent= models.ForeignKey('self',on_delete=models.CASCADE ,blank=True,null=True,related_name='+')
    body = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.blog.title)
    @property
    def children(self):
        return Blog_Comment.objects.filter(parent=self).order_by('created_date').all()

    # def get_absolute_url(self):
    #     return reverse("blogs",)

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


# Create your models here.
