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


import matplotlib as mpl
mpl.use('Agg')

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

import vfatserver.consts as consts
import vfatserver.util as util
from .util import plot_visual_field, plot_curve
from .models import EquidistantAssessment, OctopusG1Assessment


def index(request):
    equidistant_left = EquidistantAssessment.objects.filter(user=request.user, tested_eye=0).order_by('-date')
    equidistant_right = EquidistantAssessment.objects.filter(user=request.user, tested_eye=1).order_by('-date')

    octopusg1_left = OctopusG1Assessment.objects.filter(user=request.user, tested_eye=0).order_by('-date')
    octopusg1_right = OctopusG1Assessment.objects.filter(user=request.user, tested_eye=1).order_by('-date')

    context = {'equidistant_left': equidistant_left, 'equidistant_right': equidistant_right,
               'octopusg1_left': octopusg1_left, 'octopusg1_right': octopusg1_right}

    return render(request, 'assessment/index.html', context)


def detail_equidistant(request, assessment_id):
    equidistant_assessment = get_object_or_404(EquidistantAssessment, pk=assessment_id, user=request.user)


    context = {'assessment': equidistant_assessment,
               'program_url': reverse('clientconf:equidistant-update', args=[equidistant_assessment.configuration.id]),
               'field_url': reverse('assessment:detail-equidistant-field', args=[equidistant_assessment.id]),
               'curve_url': reverse('assessment:detail-equidistant-curve', args=[equidistant_assessment.id]),
               'delete_url': reverse('assessment:delete-equidistant', args=[equidistant_assessment.id])}

    return render(request, 'assessment/detail.html', context)


def detail_octopusg1(request, assessment_id):
    ocotopus_assessment = get_object_or_404(OctopusG1Assessment, pk=assessment_id, user=request.user)


    context = {'assessment': ocotopus_assessment,
               'program_url': reverse('clientconf:octopus-update', args=[ocotopus_assessment.configuration.id]),
               'field_url': reverse('assessment:detail-octopusg1-field', args=[ocotopus_assessment.id]),
               'curve_url': reverse('assessment:detail-octopusg1-curve', args=[ocotopus_assessment.id]),
               'delete_url': reverse('assessment:delete-octopusg1', args=[ocotopus_assessment.id])}

    return render(request, 'assessment/detail.html', context)


def detail_equidistant_field(request, assessment_id):
    assessment = get_object_or_404(EquidistantAssessment, pk=assessment_id, user=request.user)

    fig = plot_visual_field(assessment)

    return util.fig_to_svg_response(fig)


def detail_octopusg1_field(request, assessment_id):
    assessment = get_object_or_404(OctopusG1Assessment, pk=assessment_id, user=request.user)

    fig = plot_visual_field(assessment)

    return util.fig_to_svg_response(fig)


def detail_equidistant_curve(request, assessment_id):
    assessment = get_object_or_404(EquidistantAssessment, pk=assessment_id, user=request.user)

    fig = plot_curve(assessment)

    return util.fig_to_svg_response(fig)


def detail_octopusg1_curve(request, assessment_id):
    assessment = get_object_or_404(OctopusG1Assessment, pk=assessment_id, user=request.user)

    fig = plot_curve(assessment)

    return util.fig_to_svg_response(fig)


def delete_equidistant(request, assessment_id):
    assessment = get_object_or_404(EquidistantAssessment, user=request.user, pk=assessment_id)

    if request.method == 'POST':
        if request.user.username != consts.demo_user_name:
            assessment.delete()
            return redirect('assessment:index')
        else:
            return render(request, 'assessment/delete.html',
                          context={'assessment': assessment,
                                   'back_url': reverse('assessment:detail-equidistant', args=[assessment.id]),
                                   'message': 'Demo assessments cannot be deleted!'})
    else:
        return render(request, 'assessment/delete.html',
                      context={'assessment': assessment,
                               'back_url': reverse('assessment:detail-equidistant', args=[assessment.id])})


def delete_octopusg1(request, assessment_id):
    assessment = get_object_or_404(OctopusG1Assessment, user=request.user, pk=assessment_id)

    if request.method == 'POST':
        if request.user.username != consts.demo_user_name:
            assessment.delete()
            return redirect('assessment:index')
        else:
            return render(request, 'assessment/delete.html',
                          context={'assessment': assessment,
                                   'back_url': reverse('assessment:detail-octopusg1', args=[assessment.id]),
                                   'message': 'Demo assessments cannot be deleted!'})
    else:
        return render(request, 'assessment/delete.html',
                      context={'assessment': assessment,
                               'back_url': reverse('assessment:detail-octopusg1', args=[assessment.id])})
