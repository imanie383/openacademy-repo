# -*- coding: utf-8 -*-

from psycopg2 import IntegrityError
from openerp.tests.common import TransactionCase
from openerp.tools import mute_logger


class GlobalTestOpenAcademyCourse(TransactionCase):
    def setUp(self):
        super(GlobalTestOpenAcademyCourse, self).setUp()
        self.variable = 'Hello world'
        self.course = self.env['openacademy.course']

    def create_course(self, course_name, course_description,
                      course_responsible_id):
        course_id = self.course.create({
            'name': course_name,
            'description': course_description,
            'responsible_id': course_responsible_id
        })
        return course_id

    # Method of test startswith 'def test_*(self) : '

    # Mute error odoo.sql_db to avoid the error log
    @mute_logger('odoo.sql_db')
    def test_10_same_name_description(self):
        '''
        Test create a course with same name and description
        To test constraint of name different to description
        '''
        # Error raised expected with message expected
        with self.assertRaisesRegexp(
            IntegrityError,
            'new row for relation "openacademy_course" violates '
            'check constraint "openacademy_course_name_description_check"'
        ):
            # Create a course with same name and description to raise error
            self.create_course('test', 'test', None)

    @mute_logger('odoo.sql_db')
    def test_20_two_courses_same_name(self):
        '''
        Test to create two courses with same name.
        To raise constraint of unique name.
        '''
        new_id = self.create_course('test_name1', 'test_description1', None)
        print("new_id ", new_id)
        errorStr = 'duplicate key value violates unique constraint "openacademy_course_name_unique"'
        with self.assertRaisesRegexp(
            IntegrityError,
            errorStr
        ):
            new_id2 = self.create_course(
                'test_name1', 'test_description1', None)
            print("new_id2 ", new_id2)

    def test_15_duplicate_course(self):
        '''
        Test to duplicate course and check that works ok
        '''
        course = self.env.ref('openacademy.course0')
        course_id = course.copy()
        print("course_id", course_id)
