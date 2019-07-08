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


import random
import numpy as np

import matplotlib as mpl

mpl.use('Agg')

import matplotlib.pyplot as plt

plt.style.use('seaborn')

import vfatserver.util as util
from assessment.util import load_assessment
from assessment.models import EquidistantAssessment


def compute_training_pdf(user, eye):
    # load assessment
    assessments = EquidistantAssessment.objects.filter(user=user, tested_eye=eye) \
                      .order_by('-date')[:1]
    positions_lon_lat_radius, thresholds = load_assessment(assessments[0], cartesian_coordinates=False)
    thresholds_tested = util.sort_string_list(assessments[0].thresholds)

    # for training set not-seen (-1) to maximum brightness (0)
    thresholds[np.where(thresholds == -1)] = 0

    # bright stimuli (low values) should have high probability
    # -> invert values and then normalize so that sum is 1
    thresholds = thresholds_tested[-1] - thresholds
    pdf = thresholds / np.sum(np.sum(thresholds))
    cdf = np.cumsum(pdf)

    return positions_lon_lat_radius, pdf, cdf


def sample_coordinates(user, eye, num, jitter=0.0):
    positions_lon_lat_radius, pdf, cdf = compute_training_pdf(user, eye)

    positions_min = np.min(positions_lon_lat_radius[:, 0:2])
    positions_max = np.max(positions_lon_lat_radius[:, 0:2])
    extent = np.max([abs(positions_min), abs(positions_max)])

    random.seed()
    samples_lon_lat_radius = np.zeros((num, positions_lon_lat_radius.shape[1]))

    # Inverse transform sampling from PDF
    for i in range(0, num):
        # np.argmax returns the index where the condition is true for the first time
        index = np.argmax(cdf > random.random())
        samples_lon_lat_radius[i] = positions_lon_lat_radius[index]

    if jitter > 0:
        samples_lon_lat_radius[:, 0:2] = np.multiply(samples_lon_lat_radius[:, 0:2],
                                             np.random.normal(1.0, jitter, size=samples_lon_lat_radius[:, 0:2].shape))

        samples_lon_lat_radius[np.where(samples_lon_lat_radius[:, 0:2] > extent)] = extent
        samples_lon_lat_radius[np.where(samples_lon_lat_radius[:, 0:2] < -extent)] = -extent

    return samples_lon_lat_radius
