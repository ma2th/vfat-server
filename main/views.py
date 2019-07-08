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


from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from registration.backends.simple.views import RegistrationView

from assessment.models import Assessment, BasicProgram
import vfatserver.consts as consts


def index(request):
    return render(request, 'main/index.html')


def delete_account(request):
    if request.method == 'POST':
        if request.user.username != consts.demo_user_name:
            assessments = Assessment.objects.filter(user = request.user)
            programs = BasicProgram.objects.filter(user = request.user)

            assessments.delete()
            programs.delete()
            request.user.delete()

            return redirect('home')
        else:
            return render(request, 'registration/delete_account.html',
                          context={'message': 'The demo account cannot be deleted!'})
    else:
        return render(request, 'registration/delete_account.html')


class CustomRegistrationView(RegistrationView):
    success_url = reverse_lazy('main:index')

