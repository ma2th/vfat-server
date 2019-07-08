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


import io
import math
import descartes
import numpy as np
import shapely.geometry as sg
import matplotlib.pyplot as plt

from django.http import HttpResponse


def sort_string_list(list_as_string):
    values_as_list = np.array(list_as_string.split(' '))
    values_as_list = values_as_list.astype(float)
    values_as_list = np.sort(values_as_list)

    return values_as_list


def geographic_to_cartesian(np_array):
    result = np.stack([np_array[:, 2] * np.cos(np.radians(np_array[:, 1])) * np.cos(np.radians(np_array[:, 0])),
                       np_array[:, 2] * np.cos(np.radians(np_array[:, 1])) * np.sin(np.radians(np_array[:, 0])),
                       np_array[:, 2] * np.sin(np.radians(np_array[:, 1]))])

    return result.transpose()


def points_on_circle(radius, num):
    return [[math.cos(2 * math.pi / num * x) * radius, math.sin(2 * math.pi / num * x) * radius]
            for x in range(0, num)]


def fig_to_svg_response(fig):
    # response = HttpResponse(content_type='image/svg+xml')
    # fig.savefig(response, format='svg', bbox_inches='tight', pad_inches=0)
    # plt.close(fig)

    buf = io.BytesIO()
    plt.savefig(buf, format='svg')
    plt.close(fig)
    response = HttpResponse(buf.getvalue(), content_type='image/svg+xml')

    return response


def create_negative_circle_patch(radius, x1, y1, x2, y2, color='w'):
    circle = sg.Point(0, 0).buffer(radius)
    rectangle = sg.box(x1, y1, x2, y2)
    diff = rectangle.difference(circle)

    return descartes.PolygonPatch(diff, facecolor=color, edgecolor=color)
