from django.test import TestCase
from django.urls import reverse, resolve
from shopping.views import Top, CreateToDo, EditToDo, DeleteToDo


class ShoppingUrlsTests(TestCase):
    def test_top_url_resolves(self):
        """Test 'top' url resolves to the correct view."""
        url = reverse('shopping:top')
        self.assertEqual(resolve(url).func.view_class, Top)

    def test_create_todo_url_resolves(self):
        """Test 'create_todo' url resolves to the correct view."""
        url = reverse('shopping:create_todo')
        self.assertEqual(resolve(url).func.view_class, CreateToDo)

    def test_edit_todo_url_resolves(self):
        """Test 'edit_todo' url with a pk resolves to the correct view."""
        url = reverse('shopping:edit_todo', args=[1])
        self.assertEqual(resolve(url).func.view_class, EditToDo)

    def test_delete_todo_url_resolves(self):
        """Test 'delete_todo' url with a pk resolves to the correct view."""
        url = reverse('shopping:delete_todo', args=[1])
        self.assertEqual(resolve(url).func.view_class, DeleteToDo)