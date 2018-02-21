# -*- coding: utf-8 -*-

from psycopg2 import IntegrityError
from openerp.tests.common import TransactionCase
from openerp.tools import mute_logger

class GlobalTestOpenAcademyCourse(TransactionCase):
    def setUp(self):
        super(GlobalTestOpenAcademyCourse,self).setUp()
        self.variable = 'Hello world'
        self.course = self.env['openacademy.course']

    def create_course(self,course_name,course_description,
                      course_responsible_id):
        course_id = self.course.create({
            'name' : course_name,
            'description' : course_description,
            'responsible_id' :course_responsible_id
        })
        return course_id

    #Method of test startswith 'def test_*(self) : '

    @mute_logger('odoo.sql_db')
    def test_01_same_name_description(self):
        '''
        Test create a course with same name and description.
        To test constraint of name different to description
        '''
        with self.assertRaisesRegexp(
            IntegrityError,
            'new row for relation "openacademy_course" violates '
            'check constraint "openacademy_course_name_description_check"'
        ):
            self.create_course('test','test',None)