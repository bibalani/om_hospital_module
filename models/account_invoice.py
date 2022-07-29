from odoo import models, fields, api, _

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    so_confirmed_user_id = fields.Many2one('res.users', string="So Confirmed User")


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"   

    line_number  = fields.Integer(string="Line Number") 
