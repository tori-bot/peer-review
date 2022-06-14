from sre_parse import CATEGORIES
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)   
    profile_picture=models.ImageField(upload_to='profile_pictures/',default='default.jpg',null=True) 
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


CATEGORIES=(
    ('technology', 'technology'),
    ('art', 'art'),
    ('fashion', 'fashion'),
    ('architecture', 'architecture'),
)
class Project(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/',default='default.png')
    description=models.TextField()
    git_url = models.URLField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    published=models.DateTimeField(auto_now_add=True)
    category=models.CharField(max_length=30,choices=CATEGORIES,default='technology',null=True)

    def save_picture(self):
        self.save()

    def delete_picture(self):
        self.delete()

    def update_project(self,title,image,description,git_url,user,published):
        self.title=title
        self.image=image
        self.description=description
        self.git_url=git_url
        self.user=user
        self.published=published
        self.save()

    @classmethod
    def get_project_by_id(cls,id):
        project=cls.objects.get(id=id)
        return project

    def search_project(cls,search_term):
        projects=cls.objects.filter(title__icontains=search_term) 
        return projects

    def __str__(self):
        return self.title
