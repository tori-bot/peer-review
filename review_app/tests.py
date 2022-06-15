from django.test import TestCase
from . models import *
# Create your tests here.
class ProjectTestClass(TestCase):
    def setUp(self):
        self.project = Project(name='reviews_app')

    def test_instance(self):
        self.assertTrue(isinstance(self.project,Project))

    def test_save_project(self):
        self.project.save_project()
        project=Project.objects.all()
        self.assertTrue(len(project))

    def test_delete_project(self):
        self.project.save_project()
        self.project.delete_project()
        project=Project.objects.all()
        self.assertTrue(len(project)==0)

class ProfileTestCase(TestCase):
    def setUp(self):
        self.projects = Project(name='review_app')
        self.projects.save_project()
        self.profile = Profile(bio='this is a bio',author='Author',
        email='testemail@gmail.com',projects=self.projects)

    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_save_profile(self):
        self.profile.save_profile()
        profile=Profile.objects.all()
        self.assertTrue(len(profile))

    def test_delete_profile(self):
        self.profile.save_profile()
        self.profile.delete_profile()
        profile=Project.objects.all()
        self.assertTrue(len(profile))

# Create your tests here.
