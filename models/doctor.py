from odoo import models, api, fields, _


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ["mail.thread","mail.activity.mixin"]
    _description = "Hospital Doctor"
    _rec_name = "doctor_name"


    @api.model
    def default_get(self, fields):
        res = super(HospitalDoctor, self).default_get(fields)
        # res return a dictionary of default value
        if not res.get('gender'):
            res['gender'] = 'female'
        return res
    # As 'gender' field is not included in tree view, singeleton error is not going to happen         

    doctor_name = fields.Char(string="Doctor")
    related_user_id = fields.Many2one('res.users', string="Related User", required=True)
    age = fields.Integer(string="Age", copy=False)
    gender = fields.Selection([('male','Male'),('female','Female'),('other', 'Other')], string="Gender",
    tracking=True)
    note = fields.Char("Description")
    appointment_ids = fields.One2many("hospital.appointment", "doctor_id", string="Appointments")
    working_hospital_boss_id = fields.Many2one('res.partner', string="Working Hospital Boss")


    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "New Doctor"
        res  = super(HospitalDoctor, self).create(vals) 
        return res  


 


    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get("doctor_name"):
            default["doctor_name"] = self.doctor_name + _(" (Copy)")
        if not default.get("note"):
            default["note"] = _("(Coppied Record)")        
        return super(HospitalDoctor, self).copy(default)
