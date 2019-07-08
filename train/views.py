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


import numpy as np
import matplotlib as mpl

mpl.use('Agg')

import matplotlib.pyplot as plt

plt.style.use('seaborn')

from django.shortcuts import render

import vfatserver.util as util
from vfatserver import consts
from .util import compute_training_pdf, sample_coordinates
from assessment.util import plot_assessment
from assessment.models import EquidistantAssessment


def left_eye(request):
    return process_eye(request, 0)


def right_eye(request):
    return process_eye(request, 1)


def process_eye(request, eye):
    # get data
    positions_lon_lat_radius, pdf, _ = compute_training_pdf(request.user, eye)
    positions_xyz = util.geographic_to_cartesian(positions_lon_lat_radius)
    positions_xy = positions_xyz[:, 1:3]  # discard depth / orthographic projection

    # plot
    normalizer = mpl.colors.Normalize(vmin=np.min(np.min(0)),
                                      vmax=np.max(np.max(pdf)))
    fig, _, _ = plot_assessment(positions_xy, pdf, normalizer, 'winter_r')

    # visualize samples for verification purposes
    samples_lon_lat_radius = sample_coordinates(request.user, eye, 50, consts.training_jitter)
    samples_xyz = util.geographic_to_cartesian(samples_lon_lat_radius)
    samples_xy = samples_xyz[:, 1:3]  # discard depth / orthographic projection
    fig.axes[0].scatter(samples_xy[:, 0], samples_xy[:, 1], marker='x', facecolor='k', alpha=0.8)

    return util.fig_to_svg_response(fig)


def index(request):
    left = EquidistantAssessment.objects.filter(user=request.user, tested_eye=0).count()
    right = EquidistantAssessment.objects.filter(user=request.user, tested_eye=1).count()

    return render(request, 'train/index.html', {'left': left >= 1,
                                                'right': right >= 1})
