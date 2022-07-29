from odoo import models, fields, api, _

# Inherited model
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.users', string="Confirmed User")
    sale_description = fields.Char(string="Sale Description")
    approver_id = fields.Many2one('res.partner', string="Approver")


    # Inheriting method from sale.order
    def action_confirm(self):
        print("Success.....................")
        self.confirmed_user_id = self.env.user
        super(SaleOrder, self).action_confirm()
       

