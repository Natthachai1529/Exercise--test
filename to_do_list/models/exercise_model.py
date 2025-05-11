from odoo import models, fields, api

class ExampleModel(models.Model):
    _name = 'exercise.model'
    _description = 'Model for Exercise'

    title = fields.Char(string='Title')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    state = fields.Selection([
        ('draft', 'DRAFT'),
        ('in_progress', 'IN PROGRESS'),
        ('complete', 'COMPLETE'),
    ], default='draft')

    tag_ids = fields.Many2many(comodel_name='exercise.tag', string='Tags')
    list_ids = fields.One2many(comodel_name='model.list', inverse_name='list_id', string='Lists')
    attendee_ids = fields.One2many(comodel_name='model.attendee', inverse_name='attendee_id', string='Attendees')

    def action_set_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_set_in_complete(self):
        self.write({'state': 'complete'}) 

    all_complete = fields.Boolean(string='All List Completed', compute='_compute_all_complete')

    @api.depends('list_ids.is_complete')
    def _compute_all_complete(self):
        for record in self:
            if not record.list_ids:
                record.all_complete = False
            else:
                record.all_complete = all(line.is_complete for line in record.list_ids)

class ExerciseTag(models.Model):
    _name = 'exercise.tag'
    _description = 'Tag for Exercise'

    name = fields.Char(string='Tag Name', required=True)

class ListModel(models.Model):
    _name = 'model.list'
    _description = 'Model for List'

    list_id = fields.Many2one(comodel_name='exercise.model', inverse_name='list_ids', string='Exercises')
    name = fields.Char(string='Name')
    description = fields.Char(string="Description") 
    is_complete = fields.Boolean(string='Is Complete')
    tag_ids = fields.Many2many(comodel_name='exercise.tag', string='Tags')  # If you need tags for lists

class AttendeeModel(models.Model):
    _name = 'model.attendee'
    _description = 'Model for Attendees'

    attendee_id = fields.Many2one(comodel_name='exercise.model', inverse_name='attendee_ids', string='Exercise')
    attendee = fields.Many2one(comodel_name='res.partner', string='Attendee')
