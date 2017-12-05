from odoo import fields, models, api

class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    school = fields.Boolean('School', default=False)

    school_ids = fields.Many2many('school.register', string = 'Schools')