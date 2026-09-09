from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Favorite, Motorcycle

User = get_user_model()


class ShopImprovementsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='shoptester', password='pass12345')
        self.category = Category.objects.create(name='Sport', slug='sport')
        self.motorcycle = Motorcycle.objects.create(
            name='Test Bike',
            brand='honda',
            model_year=2025,
            price=1000,
            description='Test',
            image='motorcycles/test.jpg',
            category=self.category,
            stock=3,
            engine_cc=500,
            slug='test-bike',
        )

    def test_product_detail_increments_views(self):
        self.client.get(reverse('product_detail', args=[self.motorcycle.slug]))
        self.motorcycle.refresh_from_db()
        self.assertEqual(self.motorcycle.views_count, 1)

    def test_favorite_toggle_requires_login(self):
        response = self.client.post(reverse('toggle_favorite', args=[self.motorcycle.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_user_can_add_and_remove_favorite(self):
        self.client.force_login(self.user)
        url = reverse('toggle_favorite', args=[self.motorcycle.slug])
        self.client.post(url)
        self.assertTrue(Favorite.objects.filter(user=self.user, motorcycle=self.motorcycle).exists())
        self.client.post(url)
        self.assertFalse(Favorite.objects.filter(user=self.user, motorcycle=self.motorcycle).exists())

class ReviewsAndOrdersTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reviewer', password='pass12345')
        self.other_user = User.objects.create_user(username='other', password='pass12345')
        self.category = Category.objects.create(name='Touring', slug='touring')
        self.motorcycle = Motorcycle.objects.create(
            name='Review Bike', brand='yamaha', model_year=2026, price=2000,
            description='Review test', image='motorcycles/review.jpg',
            category=self.category, stock=2, engine_cc=700, slug='review-bike',
        )

    def test_user_can_create_and_update_single_review(self):
        from .models import Review
        self.client.force_login(self.user)
        url = reverse('add_review', args=[self.motorcycle.slug])
        self.client.post(url, {'rating': 5, 'comment': 'ممتازة'})
        self.assertEqual(Review.objects.filter(user=self.user, motorcycle=self.motorcycle).count(), 1)
        self.client.post(url, {'rating': 4, 'comment': 'جيدة جداً'})
        review = Review.objects.get(user=self.user, motorcycle=self.motorcycle)
        self.assertEqual(review.rating, 4)
        self.assertEqual(Review.objects.filter(user=self.user, motorcycle=self.motorcycle).count(), 1)

    def test_review_requires_login(self):
        response = self.client.post(reverse('add_review', args=[self.motorcycle.slug]), {'rating': 5, 'comment': 'x'})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_order_detail_is_private_to_owner(self):
        from .models import Order
        order = Order.objects.create(user=self.user, total=2000, shipping_address='A', phone='123', status='pending')
        self.client.force_login(self.other_user)
        response = self.client.get(reverse('order_detail', args=[order.id]))
        self.assertEqual(response.status_code, 404)

    def test_invalid_numeric_filter_does_not_crash(self):
        response = self.client.get(reverse('product_list'), {'min_price': 'not-a-number', 'min_cc': 'bad'})
        self.assertEqual(response.status_code, 200)


class ProductManagementPermissionTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import Permission
        self.category = Category.objects.create(name='Admin Category', slug='admin-category')
        self.motorcycle = Motorcycle.objects.create(
            name='Admin Bike', brand='honda', model_year=2026, price=5000,
            description='Admin test', image='motorcycles/admin.jpg',
            category=self.category, stock=2, engine_cc=600, slug='admin-bike',
        )
        self.normal_user = User.objects.create_user(username='normal', password='pass12345')
        self.staff_user = User.objects.create_user(username='staff', password='pass12345', is_staff=True)
        self.superuser = User.objects.create_superuser(username='root', email='root@example.com', password='pass12345')
        self.staff_user.user_permissions.add(*Permission.objects.filter(
            codename__in=['view_motorcycle', 'add_motorcycle', 'change_motorcycle', 'delete_motorcycle'],
            content_type__app_label='shop',
        ))

    def test_normal_user_cannot_access_product_management(self):
        self.client.force_login(self.normal_user)
        self.assertEqual(self.client.get(reverse('manage_products')).status_code, 403)
        self.assertEqual(self.client.get(reverse('product_create')).status_code, 403)
        self.assertEqual(self.client.get(reverse('product_update', args=[self.motorcycle.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse('product_delete', args=[self.motorcycle.pk])).status_code, 403)

    def test_staff_with_permissions_can_access_product_management(self):
        self.client.force_login(self.staff_user)
        self.assertEqual(self.client.get(reverse('manage_products')).status_code, 200)
        self.assertEqual(self.client.get(reverse('product_create')).status_code, 200)
        self.assertEqual(self.client.get(reverse('product_update', args=[self.motorcycle.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse('product_delete', args=[self.motorcycle.pk])).status_code, 200)

    def test_superuser_can_delete_product(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse('product_delete', args=[self.motorcycle.pk]))
        self.assertRedirects(response, reverse('manage_products'))
        self.assertFalse(Motorcycle.objects.filter(pk=self.motorcycle.pk).exists())


class AdminEmailUsersTests(TestCase):
    def setUp(self):
        self.normal_user = User.objects.create_user(username='mailnormal', email='normal@example.com', password='pass12345')
        self.staff_user = User.objects.create_user(username='mailstaff', email='staff@example.com', password='pass12345', is_staff=True)
        self.recipient = User.objects.create_user(username='recipient', email='recipient@example.com', password='pass12345')

    def test_normal_user_cannot_open_email_page(self):
        self.client.force_login(self.normal_user)
        self.assertEqual(self.client.get(reverse('send_user_email')).status_code, 403)

    def test_staff_can_open_email_page(self):
        self.client.force_login(self.staff_user)
        self.assertEqual(self.client.get(reverse('send_user_email')).status_code, 200)

    def test_staff_can_send_and_log_email(self):
        from django.test import override_settings
        from django.core import mail
        from .models import SentEmail

        self.client.force_login(self.staff_user)
        with override_settings(
            EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
            EMAIL_HOST_USER='site@example.com',
            EMAIL_HOST_PASSWORD='test-app-password',
            DEFAULT_FROM_EMAIL='site@example.com',
            CONTACT_EMAIL='site@example.com',
        ):
            response = self.client.post(reverse('send_user_email'), {
                'recipient': self.recipient.pk,
                'subject': 'اختبار',
                'message': 'هذه رسالة اختبار',
            })
        self.assertRedirects(response, reverse('send_user_email'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.recipient.email])
        self.assertTrue(SentEmail.objects.filter(recipient_user=self.recipient, status='sent').exists())
