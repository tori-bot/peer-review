from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)   
    profile_picture=models.ImageField(upload_to='profile_pictures/',null=True) 
    bio=models.TextField()
    
    @receiver(post_save, sender=User) 
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()

    def delete_profile(self):
        self.delete()

    def update_profile(self,user,profile_picture,bio):
        self.user=user
        self.profile_picture=profile_picture
        self.bio=bio
        self.save()

    @classmethod
    def get_profile_by_id(cls,id):
        profile = Profile.objects.filter(user__id = id).first()
        return profile

    @classmethod
    def search_profile(cls,search_term):
        profile=cls.objects.filter(user__username__icontains=search_term).all()
        return profile

    def __str__(self):
        return self.user
