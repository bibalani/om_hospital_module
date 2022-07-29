from copy import copy
from traceback import TracebackException
from odoo import models, api, fields, _
from datetime import date

class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"

    name = fields.Char(string="Name", required=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient")


    def create_appointment_action(self):
        print("An appointment is being created...")


   


