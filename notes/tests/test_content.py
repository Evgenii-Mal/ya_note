from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
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
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.url = reverse('notes:list')
        cls.add_url = reverse('notes:add')
        cls.edit_url = reverse('notes:edit', args=(cls.notes.slug,))

    def test_note_in_object_list_author(self):
        response = self.author_client.get(self.url)
        self.assertIn(self.notes, response.context['object_list'])

    def test_note_is_not_in_object_list_for_another_user(self):
        response = self.reader_client.get(self.url)
        self.assertNotIn(self.notes, response.context['object_list'])

    def test_pages_contain_form(self):
        urls = (
            self.add_url,
            self.edit_url,
        )
        for url in urls:
            with self.subTest(url=url):
                self.client.force_login(self.author)
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                form = response.context['form']
                self.assertIsInstance(form, NoteForm)
