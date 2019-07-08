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


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_framework_views

from .views import EquidistantAssessmentList, EquidistantProgramViewSet, OctopusG1AssessmentList, \
    OctopusG1ProgramViewSet, TrainingProgramViewSet


app_name = 'api'

router = DefaultRouter()
router.register(r'program/equidistant', EquidistantProgramViewSet, base_name='EquidistantProgram')
router.register(r'program/octopusg1', OctopusG1ProgramViewSet, base_name='OctopusG1Program')
router.register(r'program/training', TrainingProgramViewSet, base_name='TrainingProgram')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/assessment/equidistant/', EquidistantAssessmentList.as_view()),
    path('v1/assessment/octopusg1/', OctopusG1AssessmentList.as_view()),
    path('v1/token/', rest_framework_views.obtain_auth_token, name='get_auth_token'),
]
