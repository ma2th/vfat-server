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


from rest_framework import generics
from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser

from assessment.models import EquidistantSphereProgram, OctopusG1Program
from train.models import TrainingProgram

from .serializers import EquidistantAssessmentSerializer, EquidistantProgramListSerializer, \
    EquidistantProgramDetailSerializer, OctopusG1ProgramListSerializer, OctopusG1ProgramDetailSerializer, \
    OctopusG1AssessmentSerializer, TrainingProgramListSerializer, TrainingProgramDetailSerializer


class AbstractAssessmentList(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, file=self.request.data.get('file'))


class EquidistantAssessmentList(AbstractAssessmentList):
    serializer_class = EquidistantAssessmentSerializer


class OctopusG1AssessmentList(AbstractAssessmentList):
    serializer_class = OctopusG1AssessmentSerializer


class EquidistantProgramViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return EquidistantSphereProgram.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return EquidistantProgramListSerializer
        else:
            return EquidistantProgramDetailSerializer


class OctopusG1ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return OctopusG1Program.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return OctopusG1ProgramListSerializer
        else:
            return OctopusG1ProgramDetailSerializer


class TrainingProgramViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return TrainingProgram.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return TrainingProgramListSerializer
        else:
            return TrainingProgramDetailSerializer
