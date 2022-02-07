from array import ArrayType
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Django signal Import
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid

# Create your models here.

# Questions taken from the domain recruiters and pushed into database of this model.
# Both for Form responses and form filling frontend (questions and options) can be taken from here to display.
CHOICES_QTYPE = [
    ('SingleChoice', 'SingleChoice'),
    ('MultipleChoice', 'MultipleChoice'),
    ('Answer', 'Answer'),
]

CHOICES_DOMAIN = [
    ('All', 'All'),
    ('Web', 'Web'),
    ('Core', 'Core'),
    ('Design', 'Design'),
    ('Docs', 'Docs'),
    ('PR', 'PR'),
]


class Questions(models.Model):
    question = models.CharField(max_length=1000)
    question_id = models.AutoField(primary_key=True)
    question_type = models.CharField(max_length=1000, choices=CHOICES_QTYPE)
    question_for_domain = models.CharField(
        max_length=1000, choices=CHOICES_DOMAIN)
    option1 = models.CharField(max_length=1000, blank=True)
    option2 = models.CharField(max_length=1000, blank=True)
    option3 = models.CharField(max_length=1000, blank=True)
    option4 = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.question


class Recruitment(models.Model):
    is_started = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return '{0}'.format(self.is_started)


# Every candidates responses
class SubmittedUser(models.Model):
    candidate_name = models.CharField(max_length=1000)
    candidate_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, auto_created=True, unique=True)
    candidate_mobile_number = models.CharField(max_length=10)
    candidate_emailid = models.EmailField()
    # Limiting the choices to only two.
    candidate_domain_choices = ArrayField(
        models.CharField(max_length=100, blank=True), size=2)
    candidate_studying_year = models.IntegerField()
    candidate_branch = models.CharField(max_length=20)

    def __str__(self):
        return self.candidate_name


'''
class FormResponses(models.Model):
    submitted_candidate_id = models.ForeignKey(
        SubmittedUser, on_delete=models.CASCADE, null=True)
    submissions = ArrayField()
'''


class FormResponses(models.Model):
    question_id = models.ForeignKey(
        Questions, on_delete=models.CASCADE, null=True)
    submitted_candidate_id = models.ForeignKey(
        SubmittedUser, on_delete=models.CASCADE, null=True)
    answer_given = models.CharField(max_length=20000, blank=True)

    def __str__(self):
        return self.submitted_candidate_id.candidate_name


# Saving the emails and phone numbers to Global level Email and Phone number DB
# @receiver(post_save,sender=FormResponses)
# def global_email(created,instance,*args,**kwargs):
#     if created:
#         ## For Global level Email save
#         pass
