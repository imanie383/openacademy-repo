# -*- coding: utf-8 -*-

from odoo import models, fields, api


def get_uid(self, *a):
    return self.env.uid


class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one(
        'res.users', string="Responsible",
        index=True, ondelete='set null',
        default=get_uid)
    session_ids = fields.One2many('openacademy.session', 'course_id')

    _sql_constraints = [
        ('name_description_check', 'CHECK(name != description)',
         "The title of the course shouldn't be the description"),

        ('name_unique', 'UNIQUE(name)',
            "The course title must be unique")
    ]

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        print("Im passing through the copy inherited function of courses")
        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)
