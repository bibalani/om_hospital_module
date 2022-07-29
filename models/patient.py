from copy import copy
from traceback import TracebackException
from odoo import models, api, fields, _
from datetime import date
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread","mail.activity.mixin"]
    _description = "Hospital Patient"


    @api.model
    def default_get(self, fields):
        res = super(HospitalPatient, self).default_get(fields)
        # default_get() function returns a dictionary containing all default fields
        if not res.get('gender'):
            res["gender"] = "other"
        return res  
    # fields ------------> ['reference', 'name', 'responsible_id', 'date_of_birth', 'age', 'gender', 'active', 'note', 'message_follower_ids', 'activity_ids', 'message_ids', 'message_attachment_count']
    # res -----------> {'reference': 'New', 'gender': 'female', 'active': True}      
    


    name = fields.Char(string='Name', Tracking=True)
    related_user_id = fields.Many2one('res.users', string="Related User", required=True)
    date_of_birth = fields.Date(string="Date of Birth")
    reference = fields.Char(string='Patient Reference',copy=False,
                            default=lambda self: _("New"))
    age = fields.Integer(string='Age', compute="_compute_age", Tracking=True, store=True)
    gender = fields.Selection([('male','Male'),('female','Female'),('other', 'Other')], string='Gender', Tracking=True, default="female")
    board_status = fields.Selection([('onboard','Onboard'),('offboard','Offboard')], string='Board Status', Tracking=True, default="onboard")
    active = fields.Boolean(string="Active", default=True)
    responsible_id = fields.Many2one('res.partner', string="Responsible")
    note = fields.Char(string="Description") 
    appointment_ids = fields.One2many("hospital.appointment", "patient_id", string="Appointments")

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                today = date.today()
                rec.age = today.year - rec.date_of_birth.year - ((today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
            else:
                rec.age = 0


# override create function (create sequence and default note)
    @api.model
    def create(self, vals):
        if not vals.get("note"):
            vals["note"] = "New Patient"

        if vals.get("reference", _("New")) == _("New"):
            vals["reference"] = self.env["ir.sequence"].next_by_code("hospital.patient") or _("New")
        res = super(HospitalPatient, self).create(vals)
        return res
    # res-------> hospital.patient(11,)
    # vals------> {'reference': 'Odoo Learning', 'gender': 'female', 'active': True, 'name': 'Jimmy',
    # 'responsible_id': 35, 'date_of_birth': '2018-12-30', 'message_attachment_count': 0,
    # 'message_follower_ids': [(0, 0, {'res_model': 'hospital.patient', 'partner_id': 3, 'subtype_ids': [(6, 0, [1])]})]}    


    def write(self, vals):
        print("write method is trigerred..............", vals)
        if not self.reference and not vals.get("reference"):
            vals["reference"] = self.env["ir.sequence"].next_by_code("hospital.patient") or _("New")
        res = super(HospitalPatient, self).write(vals)
        return res
        # write method is trigerred {'date_of_birth': '2003-08-21'}



    @api.multi
    @api.constrains("name",)
    def _check_name(self):
        for rec in self:
            patient = self.env['hospital.patient'].search([('name','=',rec.name),('id',"!=",rec.id)])
            print(self.env['hospital.patient'])
            if patient:
                raise ValidationError(_("The name %s Already Exists" % rec.name))

    @api.multi
    @api.constrains("age",)
    def _check_age(self):
        for rec in self:
            print("age-------------------------->", rec.age)
            if rec.age <= 0:
                raise ValidationError(_("The Age Should be Greater Than %s" % rec.age))


    
    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            name = '[' + str(rec.reference) +  '] ' + str(rec.name)
            # I do not know why it is fixed by making rec.name string!
            result.append((rec.id, name)) 
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        domain = args + ['|',('name', operator, name),('reference', operator, name)]    
        return super(HospitalPatient,self).search(domain, limit=limit).name_get()   



# @api.depends(lambda self: (self._rec_name,) if self._rec_name else ())
# def _compute_display_name(self):
#     names = dict(self.name_get())
#     for rec in self:
#         rec.display_name = names.get(rec.id, False)




        

   


