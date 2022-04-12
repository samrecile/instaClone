from django.test import TestCase
from main.models import *
from django.core.files.uploadedfile import SimpleUploadedFile

class TestModels(TestCase):

    def setUp(self):
        test_image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        self.image1 = Image.objects.create(
            image = 'test_image',
            image_caption = 'Hey'
        )