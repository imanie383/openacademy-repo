# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from psycopg2 import IntegrityError

class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one(
    	'res.users',string="Responsible",
    	index=True, ondelete='set null',
    	default=lambda self, *a : self.env.uid)
    session_ids = fields.One2many('openacademy.session','course_id')

    _sql_constraints = [
    	('name_description_check', 'CHECK(name != description)', 
    		"The title of the course shouldn't be the description" ), 
    	('name_unique', 'UNIQUE(name)', "The course title must be unique" )
    ]

    def copy(self, default=None):
    	 if default is None:
    	 	default = {}
    	 copied_count = self.search_count(
	    	 	[
	    	 		('name','ilike','Copy of %s%%' % (self.name))
	    	 	]
	    	 )

    	 if not copied_count:
    	 	new_name = "Copy of %s" % (self.name)
    	 else:
    	 	new_name = "Copy of %s (%s)" % (self.name, copied_count)

    	 default['name'] = new_name
    	 # try:
    	 return super(Course, self).copy(default)
    	 # except exception