from odoo import models, fields, api

class CrmDateUpdateWizard(models.TransientModel):
    _name = 'crm.date.update.wizard'
    _description = 'Wizard para actualizar fecha de cierre en CRM'
    
    lead_id = fields.Many2one('crm.lead', string='Oportunidad', required=True)
    new_date = fields.Datetime(string='Nueva Fecha de Cierre', required=True)
    
    def action_update_date(self):
        self.ensure_one()
        self.lead_id.write({'date_closed': self.new_date})
        return {'type': 'ir.actions.act_window_close'}