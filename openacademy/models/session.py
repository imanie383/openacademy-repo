# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import timedelta


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    datetime_test = fields.Datetime(default=fields.Datetime.now)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one(
        'res.partner', string='Instructor',
        domain=[('instructor', '=', True)])
    course_id = fields.Many2one(
        'openacademy.course', ondelete='cascade',
        string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="attendees")
    taken_seats = fields.Float(compute='_taken_seats')
    active = fields.Boolean(default=True)
    end_date = fields.Date(
        store=True, compute='_get_end_date',
        inverse='_set_end_date')
    attendees_count = fields.Integer(
        compute='_get_attendees_count', store=True)
    color = fields.Float()
    hours = fields.Float(
        string="Duration in hours", compute='_get_hours',
        inverse='_set_hours')

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for record in self:
            record.attendees_count = len(record.attendee_ids)

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for record in self.filtered('start_date'):
            start_date = fields.Datetime.from_string(record.start_date)
            record.end_date = start_date + timedelta(
                days=record.duration, seconds=-1)

    def _set_end_date(self):
        for record in self.filtered('start_date'):
            start_date = fields.Datetime.from_string(record.start_date)
            end_date = fields.Datetime.from_string(record.end_date)
            record.duration = (end_date - start_date).days + 1

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        # import pdb; pdb.set_trace()
        for record in self.filtered(lambda r: r.seats != 0):
            percent = len(record.attendee_ids) / record.seats
            record.taken_seats = 100.0 * percent

    @api.onchange('seats', 'attendee_ids')
    def _veryfy_valid_seats(self):
        if self.seats < 0:
            self.active = False
            return {
                'warning': {
                    'title': "Incorrect seats value",
                    'message': "The number of \
                    available seats may not be negative"
                }
            }

        if self.seats < len(self.attendee_ids):
            self.active = False
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees"
                }
            }

    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for record in self.filtered('instructor_id'):
            if record.instructor_id in record.attendee_ids:
                raise exceptions.ValidationError(
                    "A session's instructor can't be an attendee")
