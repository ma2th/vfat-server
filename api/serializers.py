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


from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from assessment.models import EquidistantAssessment, \
    OctopusG1Assessment, \
    EquidistantSphereProgram, \
    OctopusG1Program
from train.models import TrainingProgram


class AbstractProgramListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')


class AbstractAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('duration', 'configuration', 'false_positive', 'file',
                  'tested_eye', 'blind_spot_false_positive')


class EquidistantProgramListSerializer(AbstractProgramListSerializer):
    class Meta(AbstractProgramListSerializer.Meta):
        model = EquidistantSphereProgram


class EquidistantProgramDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquidistantSphereProgram
        exclude = ('user',)


class EquidistantAssessmentSerializer(AbstractAssessmentSerializer):
    class Meta(AbstractAssessmentSerializer.Meta):
        model = EquidistantAssessment

    def validate(self, data):
        program = data['configuration']
        if program.user != self.context['request'].user:
            raise ValidationError('Program configuration not available for this user')
        return data


class OctopusG1ProgramListSerializer(AbstractProgramListSerializer):
    class Meta(AbstractProgramListSerializer.Meta):
        model = OctopusG1Program


class OctopusG1ProgramDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OctopusG1Program
        exclude = ('user',)


class OctopusG1AssessmentSerializer(AbstractAssessmentSerializer):
    class Meta(AbstractAssessmentSerializer.Meta):
        model = OctopusG1Assessment

    def validate(self, data):
        program = data['configuration']
        if program.user != self.context['request'].user:
            raise ValidationError('Program configuration not available for this user')
        return data


class TrainingProgramListSerializer(AbstractProgramListSerializer):
    class Meta(AbstractProgramListSerializer.Meta):
        model = TrainingProgram


class CoordinatesField(serializers.ListField):
    def to_representation(self, value):
        ret = []

        for coordinate in value:
            ret.append({'longitude': coordinate[0],
                        'latitude': coordinate[1],
                        'radius': coordinate[2]})

        return ret

    def to_internal_value(self, data):
        return ''


class TrainingProgramDetailSerializer(serializers.ModelSerializer):
    coordinates = CoordinatesField(source='get_coordinates', read_only=True)

    class Meta:
        model = TrainingProgram
        exclude = ('user', 'training_positions')
