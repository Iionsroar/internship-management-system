# -*- coding: utf-8 -*-

import datetime
from dateutil import rrule

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Interns(models.Model):
    _name = "internship.interns"

    INTERNSHIP_STATE = [
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
    WORKING_STATE = [
        ('project', 'Endorsing to Project...'),
        ('team', 'Assigning Team...'),
        ('ticket', 'Working on tickets...')
    ]

    intern_id = fields.Many2one('res.partner', 'Name')
    school_id = fields.Many2one('res.partner', 'School')
    email = fields.Char('Email')
    contact_no = fields.Char('Contact No.')

    supervisor_id = fields.Many2one('hr.employee', 'Supervisor')
    mentor_id = fields.Many2one('hr.employee', 'Mentor')
    project_id = fields.Many2one('project.project', 'Project')
    team_id = fields.Many2one('project.teams', 'Team')
    intern_position = fields.Selection(INTERN_POSITION, string='Intern Position')

    total_hours = fields.Integer('Total Hours', default=300)
    daily_hours = fields.Integer('Daily Hours', default=8)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

    endorsement_letter = fields.Boolean('Endorsement Letter')
    memorandum_of_agreement = fields.Boolean('Memorandum of Agreement')
    intern_agreement = fields.Boolean('Intern Agreement')

    questions_remarks = fields.Text('Questions/ Remarks')
    hr_comments = fields.Text('HR Comments')

    internship_state = fields.Selection(
        INTERNSHIP_STATE, string="Internship Status", default=INTERNSHIP_STATE[0][0]
    )
    working_state = fields.Selection(
        WORKING_STATE, string="Working Status", default=WORKING_STATE[0][0]
    )

    def onboard(self):
        self.internship_state = 'onboarding'
        if self.working_state == 'ticket':
            self.working_state = 'team'

    def work(self):
        self.internship_state = 'working'
        self.working_state = 'ticket'

    def offboard(self):
        self.internship_state = 'offboarding'
        self.working_state = 'ticket'

    def endorse_to_project(self):
        if not self.internship_state in ('working', 'offboarding'):
            self.working_state = 'project'

    def assign_team(self):
        if not self.internship_state in ('working', 'offboarding'):
            self.working_state = 'team'

    # @api.constrains('total_hours')
    # def _check_total_hours(self):
    #     if self.total_hours < 100 or self.total_hours > 1000:
    #         raise ValidationError("Total Hours must be between 100 and 1000")

    # @api.constrains('daily_hours')
    # def _check_total_hours(self):
    #     if self.daily_hours < 1 or self.daily_hours > 10:
    #         raise ValidationError("Daily Hours must be between 1 and 10")

    @api.onchange('intern_id')
    def onchange_intern_id(self):
        if self.intern_id:
            self.school_id = self.intern_id.parent_id
            self.email = self.intern_id.email
            self.contact_no = self.intern_id.phone

    @api.onchange('total_hours', 'daily_hours', 'start_date')
    def onchange_time(self):
        if self.total_hours and self.daily_hours and self.start_date:
            total_days = round(self.total_hours / self.daily_hours)
            # total_weeks = timedelta(weeks=(total_days // 5)) # 5 = regular workdays
            # excess_days = timedelta(days=(total_days % 5))
            # self.end_date = (self.start_date + total_weeks + excess_days - timedelta(days=1)) # days=1 accounts for start date

            # https://stackoverflow.com/questions/9187215/datetime-python-next-business-day
            holidays = [
                # datetime.date(2012, 5, 1,),
                # ...
            ]

            # Create a rule to recur every weekday starting the specified date
            r = rrule.rrule(rrule.DAILY,
                            byweekday=[rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR],
                            dtstart=self.start_date)

            # Create a rruleset
            rs = rrule.rruleset()

            # Attach our rrule to it
            rs.rrule(r)

            # Add holidays as exclusion days
            for exdate in holidays:
                rs.exdate(exdate)

            self.end_date = rs[total_days - 1] # subtract 1 day to account for start date

class Activities(models.Model):
    _name = "internship.activities"

    date = fields.Date('Date', default=lambda self: fields.Date.today())
    intern_id = fields.Many2one('res.partner', 'Intern')
    description = fields.Text('Description')
    duration = fields.Char('Duration', default="0:00", help="Hours:Minutes")
    impediments = fields.Text('Impediments')

    # @api.constrains('duration')
    # def _check_duration(self):
    #     if self.duration == "0:00"

class Teams(models.Model):
    _name = "project.teams"

    name = fields.Char('Name')
    project_id = fields.Many2one('project.project', 'Project')

