# Copyright 2019 Matthias Ring
# Machine Learning and Data Analytics Lab
# Friedrich-Alexander-University Erlangen-Nuremberg
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.core.validators import RegexValidator
from django.conf import settings

from datetime import datetime

from main.models import User

EYE_CHOICES = ((0, 'Left'), (1, 'Right'),)

decimal_separator = r'\.' if settings.DECIMAL_SEPARATOR == '.' else r','
float_list_validator = RegexValidator(r'^(\d+(' + decimal_separator + r')?\d* *)+$',
                                      'Please provide a white space separated list of numbers')


###
# Programs
###

class BasicProgram(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    fixation_color = models.CharField(max_length=7)
    assessment_color = models.CharField(max_length=7)
    eye = models.IntegerField(choices=EYE_CHOICES)
    max_waiting_time = models.FloatField()
    min_waiting_time = models.FloatField()
    max_response_time = models.FloatField()
    min_response_time = models.FloatField()
    display_time = models.FloatField()
    stimulus_size = models.FloatField()
    thresholds = models.CharField(max_length=512, validators=[float_list_validator])

    class Meta:
        abstract = True


class BasicAssessmentProgram(BasicProgram):
    blind_spot_tests = models.PositiveIntegerField()

    class Meta:
        abstract = True


class EquidistantSphereProgram(BasicAssessmentProgram):
    test_positions = models.IntegerField()
    max_inclination = models.FloatField()
    min_inclination = models.FloatField()


class OctopusG1Program(BasicAssessmentProgram):
    pass


###
# Assessments
###


def user_directory_path(instance, filename):
    return 'assessment/{}/{}'.format(instance.user.id, datetime.now())


class Assessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()
    tested_eye = models.IntegerField(choices=EYE_CHOICES)
    false_positive = models.PositiveIntegerField()
    blind_spot_false_positive = models.PositiveIntegerField()

    # save these configuration settings in case configuration gets updated after assessment
    blind_spot_tests = models.PositiveIntegerField()
    thresholds = models.CharField(max_length=512, validators=[float_list_validator])
    max_response_time = models.FloatField()
    min_response_time = models.FloatField()

    class Meta:
        abstract = True


class EquidistantAssessment(Assessment):
    configuration = models.ForeignKey(EquidistantSphereProgram, on_delete=models.PROTECT)


@receiver(pre_delete, sender=EquidistantAssessment)
def delete_equidistant_file(sender, instance, *args, **kwargs):
    instance.file.delete()


@receiver(pre_save, sender=EquidistantAssessment)
def equidistant_pre_save(sender, instance, *args, **kwargs):
    instance.thresholds = instance.configuration.thresholds
    instance.blind_spot_tests = instance.configuration.blind_spot_tests
    instance.min_response_time = instance.configuration.min_response_time
    instance.max_response_time = instance.configuration.max_response_time


pre_delete.connect(delete_equidistant_file, sender=EquidistantAssessment)
pre_save.connect(equidistant_pre_save, sender=EquidistantAssessment)


class OctopusG1Assessment(Assessment):
    configuration = models.ForeignKey(OctopusG1Program, on_delete=models.PROTECT)


@receiver(pre_delete, sender=OctopusG1Assessment)
def delete_octopusg1_file(sender, instance, *args, **kwargs):
    instance.file.delete()


@receiver(pre_save, sender=OctopusG1Assessment)
def octopusg1_pre_save(sender, instance, *args, **kwargs):
    instance.thresholds = instance.configuration.thresholds
    instance.blind_spot_tests = instance.configuration.blind_spot_tests
    instance.min_response_time = instance.configuration.min_response_time
    instance.max_response_time = instance.configuration.max_response_time


pre_delete.connect(delete_octopusg1_file, sender=OctopusG1Assessment)
pre_save.connect(octopusg1_pre_save, sender=OctopusG1Assessment)
