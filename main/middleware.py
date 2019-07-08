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


from django.conf import settings
from django.http import HttpResponseRedirect

import re


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        self.exceptions = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS)

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            return None

        for url in self.exceptions:
            if url.match(request.path):
                return None

        return HttpResponseRedirect(settings.LOGIN_URL + '?next=' + request.path)
