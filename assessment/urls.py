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


from django.urls import path
from django.views.decorators.cache import never_cache

from . import views

app_name = 'assessment'

urlpatterns = [
    path('', never_cache(views.index), name='index'),
    path('equidistant/<int:assessment_id>/', views.detail_equidistant, name='detail-equidistant'),
    path('equidistant/<int:assessment_id>/field', views.detail_equidistant_field, name='detail-equidistant-field'),
    path('equidistant/<int:assessment_id>/curve', views.detail_equidistant_curve, name='detail-equidistant-curve'),
    path('equidistant/delete/<int:assessment_id>/', views.delete_equidistant, name='delete-equidistant'),
    path('octopusg1/<int:assessment_id>/', views.detail_octopusg1, name='detail-octopusg1'),
    path('octopusg1/<int:assessment_id>/field', views.detail_octopusg1_field, name='detail-octopusg1-field'),
    path('octopusg1/<int:assessment_id>/curve', views.detail_octopusg1_curve, name='detail-octopusg1-curve'),
    path('octopusg1/delete/<int:assessment_id>/', views.delete_octopusg1, name='delete-octopusg1'),
]
