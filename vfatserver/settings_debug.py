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


import importlib

from vfatserver.settings import *


DEBUG = True

CSRF_COOKIE_SECURE = False

SESSION_COOKIE_SECURE = False

SECURE_SSL_REDIRECT = False

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ALLOWED_HOSTS = ['127.0.0.1', '192.168.178.44']

