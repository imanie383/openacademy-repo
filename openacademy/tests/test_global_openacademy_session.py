# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError

class GlobalTestOpenAcademySession(TransactionCase):
	# This create global test to sessions

	# Seudo-constructor method
	def setUp(self):
		super(GlobalTestOpenAcademySession,self).setUp()
		self.session = self.env['openacademy.session']
		self.partner_vauxoo = self.env.ref('base.res_partner_address_34')
		self.course = self.env.ref('openacademy.course1')
		self.partner_attendee = self.env.ref('base.res_partner_address_5')
	#Generic methods

	#Test methods
	def test_10_instructor_is_attendee(self):
		# Check that an instructor can not be an atendee
		with self.assertRaisesRegexp(
			ValidationError,
			"A session's instructor can't be an attendee"):
			self.session.create({
				'name' : 'Session test 1',
				'seats' : 1,
				'instructor_id' : self.partner_vauxoo.id,
				'attendee_ids' : [(6,0,[self.partner_vauxoo.id])],
				'course_id' : self.course.id
			})

	def test_20_wkf_done(self):
		#Check that the workflow work fine!
		session_test = self.session.create({
				'name' : 'Session test 1',
				'seats' : 1,
				'instructor_id' : self.partner_vauxoo.id,
				'attendee_ids' : [(6,0,[self.partner_attendee.id])],
				'course_id' : self.course.id
				})

		self.assertEqual(session_test.state, 'draft','Initial state should be in "draft"')