from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import Job

@receiver(pre_save,sender = Job)
def pre_save_image(sender,instance,args,**kwargs):
        if instance._state.adding and not instance.pk:
            return False
        try:
            old_image =sender.objects.get(pk=instance.pk).image
            try:
                new_image =instance.image
            except:
                new_image = None
            if not new_image == old_image:
                    import os
                    if os.path.isfile(old_image.path):
                        os.remove(old_image.path)
        except:
            pass

