from datetime import datetime, timedelta

from django.utils import timezone
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Note


User = get_user_model()


class TestListPage(TestCase):

    LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(title='Заголовок', text='Текст', author=cls.author)

    def test_note_on_page(self):
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_URL)
        object_list = response.context['object_list']
        note_count = len(object_list)
        self.assertIn(self.note, object_list)
        self.assertEqual(note_count, 1) 

    def test_note_on_other_user_page(self):
        self.client.force_login(self.reader)
        response = self.client.get(self.LIST_URL)
        object_list = response.context['object_list']
        note_count = len(object_list)
        self.assertNotIn(self.note, object_list)
        self.assertEqual(note_count, 0)
     
class TestFormPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.note = Note.objects.create(title='Заголовок', text='Текст', author=cls.author)
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.add_url = reverse('notes:add',)

    def test_edit_has_form(self):
        self.client.force_login(self.author)
        response = self.client.get(self.edit_url)
        print (response.context)
        self.assertIn('form', response.context)
        
    def test_add_has_form(self):
        self.client.force_login(self.author)
        response = self.client.get(self.add_url)
        self.assertIn('form', response.context)         


    