from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestSomething(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.reader = User.objects.create(username='reader')
        cls.author = User.objects.create(username='author')
        cls.notes = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author)
        cls.add_url = reverse('notes:add', None)

    def test_note_in_object_list_author(self):
        url = reverse('notes:list')
        user = self.author
        self.client.force_login(user)
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertIn(self.notes, object_list)

    def test_note_is_not_in_object_list_for_another_user(self):
        url = reverse('notes:list')
        user = self.reader
        self.client.force_login(user)
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertNotIn(self.notes, object_list)

    def test_edit_has_form(self):
        user = self.author
        self.client.force_login(user)
        note_from_author = Note.objects.filter(author=self.author).first()
        url = reverse('notes:edit', args=(note_from_author.slug,))
        response = self.client.get(url)
        self.assertIn('form', response.context)

    def test_add_has_form(self):
        user = self.author
        self.client.force_login(user)
        response = self.client.get(self.add_url)
        self.assertIn('form', response.context)
