from django.test import TestCase
from .models import MenuItem


class MenuItemTest(TestCase):
    def test_get_item(self):
        item = MenuItem.objects.create(
            title="IceCream", price=80, inventory=100)
        self.assertEqual(str(item), "IceCream : 80")

    def test_delete_item(self):
        item = MenuItem.objects.create(
            title="IceCream", price=80, inventory=100)
        item.delete()
        self.assertTrue(item.DoesNotExist)
