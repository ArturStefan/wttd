import hashlib
from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        email = 'henrique@bastos.net'
        pk_hash = hashlib.md5(email.encode()).hexdigest()
        self.obj = Subscription.objects.create(
            name='Henrique Bastos',
            cpf=12345678901,
            email=email,
            phone='21-996186180',
            pk_hash=pk_hash
        )
        self.resp = self.client.get('/inscricao/{}/'.format(self.obj.pk_hash))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp,
                                'subscriptions/subscription_detail.html')

    def test_context(self):
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        contents = (self.obj.name, self.obj.cpf,
                    self.obj.email, self.obj.phone)

        with self.subTest():
            for expected in contents:
                self.assertContains(self.resp, expected)


class SubscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get('/inscricao/0/')
        self.assertEqual(404, resp.status_code)
