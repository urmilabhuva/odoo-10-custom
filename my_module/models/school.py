from odoo import models, fields, api, exceptions
from datetime import date, datetime, timedelta

class School(models.Model):
    _name = 'school.register'
    _description='School involve part in Admission Process'

    _rec_name = 'school_name'




    school_name = fields.Many2one('res.partner', string="School")
    # name = fields.Char('School Name', required=True, help='Name of the School or Collage')
    course_ids = fields.Many2many('course.course', 'school_id', string='Course')
    # course_name = fields.Many2one('course.course', string='Course Name')
    # preference_id = fields.One2many('student.register', 'preference', string='Student Preference')
    total_seat = fields.Char(string='Total Seat')
    



    @api.onchange('course_ids')
    def _total_seat_by_school(self):
        total = 0
        for school_line in self:
            if school_line.course_ids:
                for course in school_line.course_ids:
                    total += course.no_seat
            else:
                total = 0
        school_line.total_seat = total
        








class Course(models.Model):
    _name = 'course.course'
    
    name = fields.Char(string='Course')
    
    school_ids = fields.Many2many('school.register', ondelete='cascade', string="School", required=True)
    min_merit = fields.Float('merit',help = 'Min merit for getting admission.')
    no_seat = fields.Integer('No of Seats', help='No. of seat in the class')
    student_id = fields.One2many('student.register', 'course_admsn', string='Student')

class Student(models.Model):
    # _inherit = 'res.users'
    _name = 'student.register'
    # _inherit = 'res.users'
    _rec_name = 'full_name'

    full_name = fields.Many2one('res.users', string="Student Full Name")
    # login = fields.Char(string="Email ID")
    # student = fields.Boolean(string="Student", default=False)
    course_admsn = fields.Many2one('course.course', string='Admission Branch')
    merit_marks = fields.Float(string='Merit Mark', help='Should be higher than Min merit')
    preference = fields.Many2one('school.register', string='Preference', help='Preference of school want to take in admission in Descending Order')  
    
    date_start = datetime.strptime('2017-12-01','%Y-%m-%d').date()
    date_end = datetime.strptime('2017-12-27','%Y-%m-%d').date()

    # date_start = datetime.strptime(date_start_val,'%Y-%m-%d').date()
    # date_end = datetime.strptime(date_end_val,'%Y-%m-%d').date()
    # help = fields.Char()
    
    @api.constrains('merit_marks')
    def check_merit_marks(self):

        for r in self:
            for m in r.course_admsn:
                print m
                min_mark = m.min_merit
                print min_mark

            if r.merit_marks <= min_mark:
                raise exceptions.ValidationError(("Merit should be higher than min Merit"))

    @api.onchange('course_admsn')
    def _onchange_course_admsn(self):
        if self.course_admsn:
            # Set default payment method (we consider the first to be the default one)
            school_preference = self.env['school.register'].search([('course_ids', 'in', self.course_admsn.ids)])
            self.preference = school_preference.ids
            # Set payment method domain (restrict to methods enabled for the journal and to selected payment type)
            return {'domain' :{'preference': [('course_ids', 'in', self.course_admsn.ids) ] }}
        # return {}
            




