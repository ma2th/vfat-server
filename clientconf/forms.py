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


import re

from django.forms import ModelForm, TextInput, Select, CheckboxInput

from assessment.models import EquidistantSphereProgram, OctopusG1Program
from train.models import TrainingProgram


class BasicProgramForm(ModelForm):
    class Meta:
        fields = ['name', 'eye', 'thresholds', 'display_time',
                  'min_waiting_time', 'max_waiting_time',
                  'min_response_time', 'max_response_time',
                  'assessment_color', 'fixation_color', 'stimulus_size']

        widgets = {
            'name': TextInput(attrs={'class': 'w-100 form-control'}),
            'eye': Select(attrs={'class': 'w-100 form-control'}),
            'thresholds': TextInput(attrs={'class': 'w-100 form-control'}),
            'display_time': TextInput(attrs={'class': 'w-100 form-control'}),
            'min_waiting_time': TextInput(attrs={'class': 'w-100 form-control'}),
            'max_waiting_time': TextInput(attrs={'class': 'w-100 form-control'}),
            'min_response_time': TextInput(attrs={'class': 'w-100 form-control'}),
            'max_response_time': TextInput(attrs={'class': 'w-100 form-control'}),
            'assessment_color': TextInput(attrs={'class': 'w-100 form-control'}),
            'fixation_color': TextInput(attrs={'class': 'w-100 form-control'}),
            'stimulus_size': TextInput(attrs={'class': 'w-100 form-control'}),
        }

        labels = {
            'display_time': 'Stimulus display time (ms)',
            'thresholds': 'Stimulus thresholds (dB)',
            'min_waiting_time': 'Minimum waiting time (ms)',
            'max_waiting_time': 'Maximum waiting time (ms)',
            'min_response_time': 'Minimum response time (ms)',
            'max_response_time': 'Maximum response time (ms)',
            'fixation_color': 'Fixation color (RGB)',
            'assessment_color': 'Assessment color (RGB)',
            'stimulus_size': 'Stimulus size (deg)'
        }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(BasicProgramForm, self).__init__(*args, **kwargs)

    def clean_thresholds(self):
        data = self.cleaned_data['thresholds']
        data = re.sub('\s+', ' ', data).strip()
        return data


class BasicAssessmentProgramForm(BasicProgramForm):
    class Meta(BasicProgramForm.Meta):
        fields = BasicProgramForm.Meta.fields + ['blind_spot_tests']

        widgets = BasicProgramForm.Meta.widgets
        widgets['blind_spot_tests'] = TextInput(attrs={'class': 'w-100 form-control'})

        labels = BasicProgramForm.Meta.labels
        labels['blind_spot_tests'] = 'Blind spot tests'


class OctopusG1Form(BasicAssessmentProgramForm):
    class Meta(BasicAssessmentProgramForm.Meta):
        model = OctopusG1Program


class EquidistantForm(BasicAssessmentProgramForm):
    class Meta(BasicAssessmentProgramForm.Meta):
        model = EquidistantSphereProgram

        fields = BasicAssessmentProgramForm.Meta.fields + ['min_inclination', 'max_inclination', 'test_positions']

        widgets = BasicAssessmentProgramForm.Meta.widgets
        widgets['min_inclination'] = TextInput(attrs={'class': 'w-100 form-control'})
        widgets['max_inclination'] = TextInput(attrs={'class': 'w-100 form-control'})
        widgets['test_positions'] = TextInput(attrs={'class': 'w-100 form-control'})

        labels = BasicAssessmentProgramForm.Meta.labels
        labels['test_positions'] = 'Number of test positions'
        labels['min_inclination'] = 'Minimum inclination (deg)'
        labels['max_inclination'] = 'Maximum inclination (deg)'


class TrainingForm(BasicProgramForm):
    class Meta(BasicProgramForm.Meta):
        model = TrainingProgram

        fields = BasicProgramForm.Meta.fields + ['training_positions', 'random_training_color', 'reinforcement']

        widgets = BasicProgramForm.Meta.widgets
        widgets['training_positions'] = TextInput(attrs={'class': 'w-100 form-control'})
        widgets['random_training_color'] = CheckboxInput(attrs={'class': 'form-control'})
        widgets['reinforcement'] = CheckboxInput(attrs={'class': 'form-control'})

        labels = BasicProgramForm.Meta.labels
        labels['training_positions'] = 'Number of training positions'
        labels['random_training_color'] = 'Random training color'
        labels['assessment_color'] = 'Training color (RGB)'
        labels['reinforcement'] = 'Reinforcement learning'
