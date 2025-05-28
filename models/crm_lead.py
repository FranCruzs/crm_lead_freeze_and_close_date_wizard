from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    def action_open_date_update_wizard(self):
        """Permitir cambiar fecha incluso en estado 41"""
        return {
            'name': 'Cambiar Fecha de Cierre',
            'type': 'ir.actions.act_window',
            'res_model': 'crm.date.update.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_lead_id': self.id},
        }
    
    @api.constrains('stage_id')
    def _check_frozen_stage(self):
        """Solo bloquear cambios de estado desde 41 a otro, excepto para usuarios con permiso especial"""
        for lead in self:
            if lead._origin.stage_id.id == 41 and lead.stage_id.id != 41:
                if not self.env.user.has_group('__export__.res_groups_155_ad38f38e'):
                    raise UserError(_('Las oportunidades en estado 41 están congeladas y no pueden cambiarse de estado'))
    
    def write(self, vals):
        """Bloquear solo cambios de estado, permitir otros campos"""
        if 'stage_id' in vals:
            # Permitir cambio si el nuevo estado es 41
            if vals['stage_id'] == 41:
                return super().write(vals)
                
            frozen_leads = self.filtered(lambda l: l.stage_id.id == 41 and l.stage_id.id != vals['stage_id'])
            if frozen_leads:
                # Verificar si el usuario pertenece al grupo especial
                if not self.env.user.has_group('__export__.res_groups_155_ad38f38e'):
                    raise UserError(_('No puedes cambiar el estado de oportunidades congeladas (IDs: %s)') % 
                                  ', '.join(frozen_leads.mapped('name')))
        return super().write(vals)
    
    def action_new_quotation(self):
        """Permitir crear cotizaciones incluso en estado 41"""
        if self.stage_id.id == 41:
            self.message_post(body=_("Se creó cotización desde oportunidad congelada"))
        return super().action_new_quotation()
