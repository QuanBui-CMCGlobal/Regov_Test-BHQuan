from django.test import TestCase
from .models import CustomUser, PatientGroup, Patient

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email='test@example.com',
            name='Test User',
            is_active=True,
            is_staff=False,
        )

    def test_email_label(self):
        field_label = self.user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_name_label(self):
        field_label = self.user._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_object_name_is_email(self):
        expected_object_name = self.user.email
        self.assertEqual(expected_object_name, str(self.user))


class PatientGroupModelTest(TestCase):
    def setUp(self):
        self.group = PatientGroup.objects.create(
            name='Test Group',
        )

    def test_name_label(self):
        field_label = self.group._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_object_name_is_name(self):
        expected_object_name = self.group.name
        self.assertEqual(expected_object_name, str(self.group))


class PatientModelTest(TestCase):
    def setUp(self):
        self.group = PatientGroup.objects.create(
            name='Test Group',
        )
        self.parent = Patient.objects.create(
            email='parent@example.com',
            name='Parent User',
            is_active=True,
            is_staff=False,
            patients_group=self.group,
            age=30,
            date_of_birth='1992-01-01',
            phone_number=1234567890,
            address='123 Main St',
            insurance_id='ABCD1234',
        )
        self.child = Patient.objects.create(
            email='child@example.com',
            name='Child User',
            is_active=True,
            is_staff=False,
            patients_group=self.group,
            parent=self.parent,
            age=5,
            date_of_birth='2018-01-01',
            phone_number=1234567890,
            address='456 Main St',
            insurance_id='EFGH5678',
        )

    def test_email_label(self):
        field_label = self.child._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_name_label(self):
        field_label = self.child._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_object_name_is_email(self):
        expected_object_name = self.child.email
        self.assertEqual(expected_object_name, str(self.child))

    def test_age_blank(self):
        field_blank = self.child._meta.get_field('age').blank
        self.assertTrue(field_blank)

    def test_date_of_birth_blank(self):
        field_blank = self.child._meta.get_field('date_of_birth').blank
        self.assertTrue(field_blank)

    def test_health_record_blank(self):
        field_blank = self.child._meta.get_field('health_record').blank
        self.assertTrue(field_blank)

    def test_phone_number_blank(self):
        field_blank = self.child._meta.get_field('phone_number').blank
        self.assertTrue(field_blank)

    def test_address_blank(self):
        field_blank = self.child._meta.get_field('address').blank
        self.assertTrue(field_blank)

    def test_insurance_id_blank(self):
        field_blank = self.child._meta.get_field('insurance_id').blank
        self.assertTrue(field_blank)

    def test_parent_relationship(self):
        parent = self.child.parent
        self.assertEqual(parent, self.parent)

    def test_group_relationship(self):
        group = self.child.patients