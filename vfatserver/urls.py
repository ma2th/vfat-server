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


from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.flatpages import views as flat_views

from main.views import CustomRegistrationView, delete_account


urlpatterns = [
    path('home/', flat_views.flatpage, {'url': '/home/'}, name='home'),
    path('main/', include('main.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', CustomRegistrationView.as_view(), name='register'),
    path('accounts/delete/', delete_account, name='delete'),
    path('assessment/', include('assessment.urls')),
    path('stats/', include('stats.urls')),
    path('clientconf/', include('clientconf.urls')),
    path('train/', include('train.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]
