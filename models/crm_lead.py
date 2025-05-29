from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    # Lista de estados congelados
    FROZEN_STAGES = [36, 37, 38, 41, 47]
    
    def action_open_date_update_wizard(self):
        """Permitir cambiar fecha incluso en estados congelados"""
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
        """Bloquear cambios de estado desde estados congelados a otros, excepto para usuarios con permiso especial"""
        for lead in self:
            if lead._origin.stage_id.id in self.FROZEN_STAGES and lead.stage_id.id not in self.FROZEN_STAGES:
                if not self.env.user.has_group('__export__.res_groups_155_ad38f38e'):
                    raise UserError(_('Las oportunidades en estados congelados no pueden cambiarse de estado'))
    
    def write(self, vals):
        """Bloquear solo cambios de estado, permitir otros campos"""
        if 'stage_id' in vals:
            # Permitir cambio si el nuevo estado está en la lista de congelados
            if vals['stage_id'] in self.FROZEN_STAGES:
                return super().write(vals)
                
            frozen_leads = self.filtered(lambda l: l.stage_id.id in self.FROZEN_STAGES and l.stage_id.id != vals['stage_id'])
            if frozen_leads:
                # Verificar si el usuario pertenece al grupo especial
                if not self.env.user.has_group('__export__.res_groups_155_ad38f38e'):
                    raise UserError(_('No puedes cambiar el estado de oportunidades congeladas (IDs: %s)') % 
                                  ', '.join(frozen_leads.mapped('name')))
        return super().write(vals)
    
    def action_new_quotation(self):
        """Permitir crear cotizaciones incluso en estados congelados"""
        if self.stage_id.id in self.FROZEN_STAGES:
            self.message_post(body=_("Se creó cotización desde oportunidad congelada"))
        return super().action_new_quotation()
