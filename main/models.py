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


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_base_user(self, email, password, **other_fields):
        if not email:
            raise ValueError('An email address is required')
        if not password:
            raise ValueError('A password is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)

        return user

    def create_user(self, email, password, **other_fields):
        user = self.create_base_user(email, password, **other_fields)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **other_fields):
        user = self.create_base_user(email, password, **other_fields)
        user.is_admin = True
        user.save(using=self._db)

        return user


class LowerCaseEmailField(models.EmailField):
    def get_prep_value(self, value):
        value = super(LowerCaseEmailField, self).get_prep_value(value)
        if value is not None:
            value = value.lower()
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        value = super().get_db_prep_value(value, connection, prepared)
        if value is not None:
            value = value.lower()
        return value


class User(AbstractBaseUser, PermissionsMixin):
    email = LowerCaseEmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = USERNAME_FIELD

    REQUIRED_FIELDS = []

    def get_short_name(self):
        return str(self)

    def get_full_name(self):
        return str(self)

    @property
    def username(self):
        return str(self)

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email

