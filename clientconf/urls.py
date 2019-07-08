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
from django.views.decorators.cache import never_cache

from .views import index, EquidistantCreate, EquidistantUpdate, EquidistantDelete, OctopusCreate, OctopusUpdate, \
    OctopusDelete, TrainingCreate, TrainingUpdate, TrainingDelete


app_name = 'clientconf'

urlpatterns = [
    path('', never_cache(index), name='index'),
    path('equidistant/<int:pk>/', never_cache(EquidistantUpdate.as_view()), name='equidistant-update'),
    path('equidistant/create/', EquidistantCreate.as_view(), name='equidistant-create'),
    path('equidistant/delete/<int:pk>/', EquidistantDelete.as_view(), name='equidistant-delete'),
    path('octopus/<int:pk>/', never_cache(OctopusUpdate.as_view()), name='octopus-update'),
    path('octopus/create/', OctopusCreate.as_view(), name='octopus-create'),
    path('octopus/delete/<int:pk>/', OctopusDelete.as_view(), name='octopus-delete'),
    path('train/<int:pk>/', never_cache(TrainingUpdate.as_view()), name='training-update'),
    path('train/create/', TrainingCreate.as_view(), name='training-create'),
    path('train/delete/<int:pk>/', TrainingDelete.as_view(), name='training-delete'),
]
