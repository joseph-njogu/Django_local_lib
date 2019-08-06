from django.core.management import call_command
from django.test import TestCase
from catalog.models import Author
from django.urls import reverse
from django.test import Client


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Njogu', last_name='Joseph')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label, 'date of birth')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'Died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1')


# class AuthorListViewTest(TestCase):
    from django.test import Client

    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f' Christian {author_id}',
                last_name=f'Surname {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 3)

    import datetime


from django.utils import timezone

from catalog.models import BookInstance, Book, Genre, Language
# Required to assign User as a borrower
from django.contrib.auth.models import User


# class LoanedBookInstancesByUserListViewTest(TestCase):

#     def setUp(self):
#         # Create two users
#         test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
#         test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

#         test_user1.save()
#         test_user2.save()

#         # Create a book
#         test_author = Author.objects.create(first_name='John', last_name='Smith')
#         test_genre = Genre.objects.create(name='Fantasy')
#         test_language = Language.objects.create(name='English')
#         test_book = Book.objects.create(
#             title='Book Title',
#             summary='My book summary',
#             isbn='ABCDEFG',
#             author=test_author,
#            # language=test_language,
#         )
# Create genre as a post-step
# genre_objects_for_book = Genre.objects.all()
# test_book.genre.set(genre_objects_for_book)
# test_book.save()

# Create 30 BookInstance objects
# number_of_book_copies = 30
# for book_copy in range(number_of_book_copies):
#     return_date = timezone.now() + datetime.timedelta(days=book_copy % 5)
#     if book_copy % 2:
#         the_borrower = test_user1
#     else:
#         the_borrower = test_user2
#     status = 'm'
# BookInstance.objects.create(book=test_book, imprint='Unlikely Imprint, 2016', due_back=return_date,
#                             borrower=the_borrower, status=status)

# def test_redirect_if_not_logged_in(self):
#     response = self.client.get(reverse('my-borrowed'))
#     self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')


from django.test import TestCase

# Create your tests here.

import datetime
from catalog.forms import RenewBookForm


class RenewBookFormTest(TestCase):

    def test_renew_form_date_in_past(self):
        """Test form is invalid if renewal_date is before today."""
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        # """Test form is invalid if renewal_\
        # date more than 4 weeks from today."""
        date = datetime.date.today() + datetime.timedelta(weeks=4) + \
            datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        """Test form is valid if renewal_date is today."""
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        """Test form is valid if renewal_date is within 4 weeks."""
        date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_field_label(self):
        """Test renewal_date label is 'renewal date'."""
        form = RenewBookForm()
        self.assertTrue(
            form.fields['renewal_date'].label is None or
            form.fields['renewal_date'].label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        """Test renewal_date help_text is as expected."""
        form = RenewBookForm()
        self.assertEqual(
            form.fields['renewal_date'].help_text,
            'Enter a date between now and 4 weeks (default 3).')
