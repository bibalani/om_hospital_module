from csv import field_size_limit
from traceback import TracebackException
from venv import create
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread","mail.activity.mixin"]
    _description = "Hospital Appointment"
    _rec_name = "reference"


    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True,
    domain="[('board_status', '=', 'onboard')]")
    gender = fields.Selection(related='patient_id.gender')
    appointment_time = fields.Datetime(string="Appointment Time", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
    reference = fields.Char(string='Reference')
    prescription = fields.Html(string="Prescription")
    priority = fields.Selection([
                                ('0','Normal'),
                                ('1','Low'),
                                ('2','High'),
                                ('3','Vey High')], string='Priority')
    state = fields.Selection([
                             ('draft','Draft'),
                             ('in_consultation','In Consultation'),
                             ('done','Done'),
                             ('cancel','Cancelled')], default="draft",
                              string='State', required=True)
                         
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string="Pharmacy Lines")                      


    # @api.model
    # def create(self, vals):
    #     if vals.get("reference", _("New")) == _("New"):
    #         vals["reference"] = self.env["ir.sequence"].next_by_code("hospital.appointment") or _("New")
    #     res = super(HospitalAppointment, self).create(vals)
    #     return res



    @api.multi
    def unlink(self):
        if self.state == 'done':
            raise ValidationError(_("You can not delete %s as it is in Done state" % self.reference))
        res = super(HospitalAppointment, self).unlink()
        return res        

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.reference = self.patient_id.reference 

    def action_test(self):
        print("The button clicked !!!!!!!")    
    

    def action_in_consultation(self):
        for rec in self:
            rec.state = "in_consultation"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_cancel(self):
        for rec in self:
            rec.state = "cancel" 

    def action_draft(self):
        for rec in self:
            rec.state = "draft" 

    # def action_search(self):
    #     for rec in self:
    #         patients = self.env['hospital.patient'].search([])
    #         print('patients....', patients) 
    #         females = self.env['hospital.patient'].search([('name','=','Mary')])
    #         print('patients....', females.name) 
    def action_test(self, vals):
        # res = self.env['hospital.patient'].search([('name','=','Mary')])
        # print('patients....', res.name)
        # print('self....', self)
        # print("self.env['hospital.patient']....", self.env['hospital.patient'])
        # print("self.env['hospital.appointment']....", self.env['hospital.patient'])


        # Result
        # self.... hospital.appointment(2,)
        # self.env['hospital.patient'].... hospital.patient()
        # self.env['hospital.appointment'].... hospital.patient()
        # Mary

        # vals = {'name':'Haward 2','date_of_birth':'07/16/2020'}
        # res = self.env['hospital.patient'].create(vals)

        # record_to_update = self.env['hospital.patient'].browse(17)
        # if record_to_update.exists():
        #     vals = {
        #         'gender' : 'male'
        #     }
        #     record_to_update.write(vals)
        female_patients = self.env['hospital.patient'].search([('gender','=','female')])
        filtered_female_patients = self.env['hospital.patient'].search([]).filtered(lambda s: s.gender == 'female')
        mapped_female_patients = self.env['hospital.patient'].search([]).mapped('name')
        mapped_sorted_female_patients = self.env['hospital.patient'].search([]).sorted(key='age').mapped('age')

        print('female_patients--------------->',female_patients)
        print('filtered_female_patients------------------------->', filtered_female_patients)
        print('mapped_female_patients------------------------->', mapped_female_patients)
        print('mapped_female_patients------------------------->', mapped_sorted_female_patients)

        return filtered_female_patients
        


                      



class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id  = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(related="product_id.list_price")
    qty = fields.Integer(string="Quantity", default=1)
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")  




    


  
