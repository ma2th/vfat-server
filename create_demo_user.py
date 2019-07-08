from django.contrib.auth import get_user_model

UserModel = get_user_model()

if not UserModel.objects.filter(email='demo@vfat.mad.tf.fau.de').exists():
    user=UserModel.objects.create_user('demo@vfat.mad.tf.fau.de', password='demo')
    user.save()