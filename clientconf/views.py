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


from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.http import Http404
from django.db import models

from .forms import EquidistantForm, OctopusG1Form, TrainingForm
from assessment.models import EquidistantSphereProgram, OctopusG1Program
from train.models import TrainingProgram


###
# Common list view
###

def index(request):
    equidistant_list = EquidistantSphereProgram.objects.filter(user=request.user).order_by('name')
    octopus_list = OctopusG1Program.objects.filter(user=request.user).order_by('name')
    training_list = TrainingProgram.objects.filter(user=request.user).order_by('name')

    context = {'equidistant_list': equidistant_list, 'octopus_list': octopus_list,
               'training_list': training_list}

    return render(request, 'clientconf/index.html', context)


###
# Base classes
###

class AbstractProgramCreate(CreateView):
    success_url = reverse_lazy('clientconf:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        return {'eye': 0,
                'thresholds': '0 10 15 20',
                'display_time': 200,
                'min_waiting_time': 1000,
                'max_waiting_time': 3000,
                'min_response_time': 300,
                'max_response_time': 750,
                'assessment_color': 'FFFFFF',
                'fixation_color': '0000FF',
                'stimulus_size': 0.43,
                }

    def get_context_data(self, **kwargs):
        context = super(AbstractProgramCreate, self).get_context_data(**kwargs)
        context['cancel_url'] = reverse('clientconf:index')
        return context


class AbstractAssessmentProgramCreate(AbstractProgramCreate):
    def get_initial(self):
        initials = super(AbstractAssessmentProgramCreate, self).get_initial()
        initials['blind_spot_tests'] = 3
        return initials


class AbstractProgramUpdate(UpdateView):
    success_url = reverse_lazy('clientconf:index')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(AbstractProgramUpdate, self).get_context_data(**kwargs)
        context['cancel_url'] = reverse('clientconf:index')

        return context


class AbstractProgramDelete(DeleteView):
    success_url = reverse_lazy('clientconf:index')
    template_name = 'clientconf/program_delete.html'

    def get_object(self, queryset=None):
        obj = super(AbstractProgramDelete, self).get_object()
        if not obj.user == self.request.user:
            raise Http404

        return obj

    def delete(self, request, *args, **kwargs):
        try:
            return super(AbstractProgramDelete, self).delete(request, *args, **kwargs)
        except models.ProtectedError as e:
            return render(request, self.template_name, context={
                'object': self.get_object(),
                'message': 'This program cannot be deleted because there are assessments linked to it.'})


###
# Equidistant Program
###

class EquidistantCreate(AbstractAssessmentProgramCreate):
    form_class = EquidistantForm
    template_name = 'clientconf/equidistant_create.html'

    def get_initial(self):
        initials = super(EquidistantCreate, self).get_initial()
        initials['name'] = 'Left Eye (100 Positions)'
        initials['test_positions'] = 100
        initials['min_inclination'] = 3
        initials['max_inclination'] = 30
        return initials


class EquidistantUpdate(AbstractProgramUpdate):
    form_class = EquidistantForm
    model = EquidistantSphereProgram
    template_name = 'clientconf/equidistant_update.html'

    def get_context_data(self, **kwargs):
        context = super(EquidistantUpdate, self).get_context_data(**kwargs)
        context['delete_url'] = reverse('clientconf:equidistant-delete',
                                        args=[self.kwargs['pk']])
        return context


class EquidistantDelete(AbstractProgramDelete):
    model = EquidistantSphereProgram


###
# Octopus Program
###

class OctopusCreate(AbstractAssessmentProgramCreate):
    form_class = OctopusG1Form
    template_name = 'clientconf/octopus_create.html'

    def get_initial(self):
        initials = super(OctopusCreate, self).get_initial()
        initials['name'] = 'Left Eye'
        # Calibrated for iPhone 6 to match Octopus 900
        initials['thresholds'] = '20.83333333 19.99 19.34 18.56363636 17.70714286 16.83684211 15.98461538 15.19230769 14.4 13.56097561 12.64814815 11.76119403 10.84782609 9.96460177 9.05309735 8.14482759 7.31730769 6.46153846 5.5483871 4.63414634 3.69811321 2.78461538 1.8313253'
        return initials


class OctopusUpdate(AbstractProgramUpdate):
    form_class = OctopusG1Form
    model = OctopusG1Program
    template_name = 'clientconf/octopus_update.html'

    def get_context_data(self, **kwargs):
        context = super(OctopusUpdate, self).get_context_data(**kwargs)
        context['delete_url'] = reverse('clientconf:octopus-delete',
                                        args=[self.kwargs['pk']])
        return context


class OctopusDelete(AbstractProgramDelete):
    model = OctopusG1Program


###
# Training Program
###


class TrainingCreate(AbstractProgramCreate):
    form_class = TrainingForm
    template_name = 'clientconf/training_create.html'

    def get_initial(self):
        initials = super(TrainingCreate, self).get_initial()
        initials['name'] = 'Train Left'
        initials['thresholds'] = '28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0'
        initials['training_positions'] = 100
        initials['random_training_color'] = True
        initials['reinforcement'] = True
        return initials


class TrainingUpdate(AbstractProgramUpdate):
    form_class = TrainingForm
    model = TrainingProgram
    template_name = 'clientconf/training_update.html'

    def get_context_data(self, **kwargs):
        context = super(TrainingUpdate, self).get_context_data(**kwargs)
        context['delete_url'] = reverse('clientconf:training-delete',
                                        args=[self.kwargs['pk']])

        return context


class TrainingDelete(AbstractProgramDelete):
    model = TrainingProgram

