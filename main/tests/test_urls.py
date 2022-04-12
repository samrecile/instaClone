from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import *

class test_index_resolves(SimpleTestCase):
   def test_list_url_is_resolved(self):
      url = reverse("index")
      print(resolve(url))
      self.assertEquals(resolve(url).func, index)

class test_explore_resolves(SimpleTestCase):
   def test_list_url_is_resolved(self):
      url = reverse("explore")
      print(resolve(url))
      self.assertEquals(resolve(url).func, explore)

class test_post_resolves(SimpleTestCase):
   def test_list_url_is_resolved(self):
      url = reverse("post")
      print(resolve(url))
      self.assertEquals(resolve(url).func, post)

class test_delete_post_resolves(SimpleTestCase):
   def test_list_url_is_resolved(self):
      url = reverse("delete_post", args=['1'])
      print(resolve(url))
      self.assertEquals(resolve(url).func, delete_post)