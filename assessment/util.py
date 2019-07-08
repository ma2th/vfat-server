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
import pandas as pd
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt

plt.style.use('seaborn')
from scipy.interpolate import griddata

import vfatserver.consts as consts
import vfatserver.util as util


def load_assessment(assessment, cartesian_coordinates=True):
    df = pd.read_csv(assessment.file.path, header=None, sep=';')

    positions = df.as_matrix(columns=[0, 1, 2])
    if cartesian_coordinates:
        positions = util.geographic_to_cartesian(positions)
    thresholds = df[3].values

    return positions, thresholds


def plot_curve(assessment):
    _, thresholds = load_assessment(assessment)

    max_rank = thresholds.size

    # remove values when stimulus was not detected
    thresholds = thresholds[np.where(thresholds != -1.0)]

    thresholds = np.flip(np.sort(thresholds), axis=0)

    # prepare labels for y axis
    tested_thresholds = util.sort_string_list(assessment.thresholds)

    fig = plt.figure(
        figsize=(consts.assessment_pixel / consts.assessment_dpi, consts.assessment_pixel / consts.assessment_dpi),
        dpi=consts.assessment_dpi)
    ax1 = fig.add_subplot(1, 1, 1)

    ax1.plot(np.arange(1, thresholds.size + 1), thresholds, color=consts.assessment_curve_color)
    ax1.set_ylabel('Absolute threshold [dB]', color=consts.assessment_curve_color)
    ax1.tick_params(axis='y', labelcolor=consts.assessment_curve_color)
    ax1.yaxis.grid(which='major', color=consts.assessment_curve_color, linestyle=':', alpha=0.3)
    ax1.set_xlim(0, max_rank + 1)
    ax1.set_xticks([1, max_rank])
    ax1.set_ylim(tested_thresholds[0], tested_thresholds[-1] + 0.1)
    ax1.set_yticks(tested_thresholds)
    ax1.set_xlabel('Rank')
    fig.tight_layout()

    return fig


def plot_visual_field(assessment):
    positions, thresholds = load_assessment(assessment)
    positions = positions[:, 1:3]  # discard depth / orthographic projection

    threshold_list = util.sort_string_list(assessment.thresholds)
    color_normalizer = mpl.colors.Normalize(vmin=-1, vmax=threshold_list[-1])

    return plot_labeled_assessment(positions, thresholds, thresholds, color_normalizer,
                                   'Legend:\nAbsolute threshold [dB]',
                                   'Color code:\nAbsolute threshold (linear)',
                                   consts.assessment_threshold_cmap)


def plot_assessment(positions, colors, color_normalizer, cmap):
    # append some values outside of the grid for nicer plots
    positions_min = np.min(positions) * consts.assessment_stretch_factor
    positions_max = np.max(positions) * consts.assessment_stretch_factor
    radius = np.max([abs(positions_min), abs(positions_max)])

    grid_x, grid_y = np.mgrid[positions_min:positions_max:(1j * consts.assessment_pixel),
                     positions_min:positions_max:(1j * consts.assessment_pixel)]
    grid = griddata(np.append(positions, util.points_on_circle(radius, consts.assessment_additional_points), axis=0),
                    np.append(colors,
                              [(np.mean(colors)) for i in range(0, consts.assessment_additional_points)]),
                    (grid_x, grid_y), method='cubic')
    grid = grid.T

    fig = plt.figure(
        figsize=(consts.assessment_pixel / consts.assessment_dpi, consts.assessment_pixel / consts.assessment_dpi),
        dpi=consts.assessment_dpi)
    fig.add_subplot(1, 1, 1)

    fig.axes[0].imshow(grid, norm=color_normalizer, cmap=cmap, origin='lower',
                       extent=(positions_min, positions_max, positions_min, positions_max),
                       interpolation="none")
    fig.axes[0].add_patch(
        util.create_negative_circle_patch(radius, positions_min, positions_min, positions_max, positions_max))

    fig.axes[0].xaxis.set_visible(False)
    fig.axes[0].yaxis.set_visible(False)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    fig.tight_layout(pad=0, h_pad=0, w_pad=0)
    fig.axes[0].set_facecolor('white')

    return fig, positions_min, positions_max


def plot_labeled_assessment(positions, thresholds, colors, color_normalizer, legend_left, legend_right, cmap):
    fig, min_pos, max_pos = plot_assessment(positions, colors, color_normalizer, cmap)

    for i in range(len(positions)):
        if thresholds[i] == -1:
            annotation = 'x'
        else:
            annotation = '{0:.1f}'.format(round(thresholds[i], 1))

        text_color = cmap(1.0) if color_normalizer(colors[i]) < 0.5 else cmap(0)
        fig.axes[0].text(positions[i, 0], positions[i, 1], annotation,
                         fontsize=5, horizontalalignment='center',
                         verticalalignment='center',
                         color=text_color)

    fig.axes[0].text(min_pos, min_pos, legend_left, fontsize=7)
    fig.axes[0].text(-min_pos, min_pos, legend_right, fontsize=7, horizontalalignment='right')

    return fig
