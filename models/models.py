# -*- coding: utf-8 -*-

# from datetime import datetime

from odoo import models, fields, api

class Interns(models.Model):
    _name = "internship.interns"

    INTERNSHIP_STATUS = [
        ('onboarding', 'Onboarding'),
        ('working', 'Working'),
        ('offboarding', 'Offboarding'),
    ]
    INTERN_POSITION = [
        ('qa_intern', 'Quality Assurance Intern'),
        ('dev_intern', 'Developer Intern'),
        ('pm_intern', 'Project Manager Intern'),
        ('admin_intern', 'Administrator Intern')
    ]

    intern_id = fields.Many2one('res.partner', 'Name')
    school_id = fields.Many2one('res.company', 'School')
    email = fields.Char('Email')
    contact_no = fields.Char('Contact No.')
    no_of_hours = fields.Integer('No. of Hours')
    internship_status = fields.Selection(INTERNSHIP_STATUS, string="Internship Status")
    project_id = fields.Many2one('project.project', 'Project')
    team_id = fields.Many2one('project.teams', 'Team')
    intern_position = fields.Selection(INTERN_POSITION, string='Intern Position')
    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('End Date')
    endorsement_letter = fields.Boolean('Endorsement Letter')
    memorandum_of_agreement = fields.Boolean('Memorandum of Agreement')
    intern_agreement = fields.Boolean('Intern Agreement')
    questions_remarks = fields.Text('Questions/ Remarks')
    hr_comments = fields.Text('HR Comments')

    @api.onchange('intern_id')
    def onchange_intern_id(self):
        if self.intern_id:
            self.school_id = self.intern_id.company_name
            self.email = self.intern_id.email
            self.contact_no = self.intern_id.phone
            self.internship_status = self.INTERNSHIP_STATUS[0][0]

    # @api.onchange('no_of_hours')
    # def onchange_no_of_hours(self):
    #     # add schedule?
    #     if self.no_of_hours and self.start_date and no_hours_daily:
    #         self.end_date = 


class Activities(models.Model):
    _name = "internship.activities"

    date = fields.Date('Date', default=lambda self: fields.Date.today())
    intern_id = fields.Many2one('res.partner', 'Intern')
    description = fields.Text('Description')
    duration = fields.Char('Duration')
    impediments = fields.Text('Impediments')

class Teams(models.Model):
    _name = "project.teams"

    name = fields.Char('Name')
    project_id = fields.Many2one('project.project', 'Project')

