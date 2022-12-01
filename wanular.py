# -*- coding: utf-8 -*-

from email.policy import default
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import calendar, datetime

class WizardAnular(models.TransientModel):
    _name = 'beca.wanular'
    _description = 'Report Wizard'

    date_start       = fields.Date('Fecha Inicio', required=True, default=fields.Date.today )
    date_end         = fields.Date('Fecha Fin', required=True, default=fields.Date.today)
    planilla_id      = fields.Many2one('beca.planilla', string="Nro. Planilla", required=True)
    nombre1_persona  = fields.Char(string='Nombre 1', related='planilla_id.nombre1', readonly=True, store=True)
    nombre2_persona  = fields.Char(string='Nombre 2', related='planilla_id.nombre2', readonly=True, store=True)
    apellido1_persona  = fields.Char(string='Apellido 1', related='planilla_id.apellido1', readonly=True, store=True)
    apellido2_persona  = fields.Char(string='Apellido 1', related='planilla_id.apellido2', readonly=True, store=True)
    cedula_persona  = fields.Char(string='Nro. Cédula', related='planilla_id.cedula', readonly=True, store=True)

    anulada_id = fields.Selection([
        ('EXTRAVIADA', 'EXTRAVIADA'),
        ('DETERIORADA', 'DETERIORADA'),
        ('NUMERO DUPLICADO', 'NUMERO DUPLICADO'),
        ('CON TACHADURAS', 'CON TACHADURAS'),
        ('OTRO', 'OTRO'),
    ], required=True, string='Motivo Anulaciòn *', help="Seleccione la Modalidad de Estudios (es campo Obligatorio).")

    note_anulada = fields.Text(string="Observaciones", help="Escriba las Observaciones (es Opcional)." )


    def action_censado(self):
        form_data = self.read()[0]

        registro  = self.env['beca.planilla'].search([('numero','=', self.planilla_id.numero)])
        planilla  = self.env['beca.planilla'].browse([registro.id])

        if planilla:
           planilla.state = 'censado'
          
        return

    def action_anular(self):
        form_data = self.read()[0]

        registro  = self.env['beca.planilla'].search([('numero','=', self.planilla_id.numero)], limit=1)
        planilla  = self.env['beca.planilla'].browse([registro.id])
        
        if planilla:
           planilla.state = 'anulada'
           planilla.anulada_id = self.anulada_id
           planilla.note_anulada = self.note_anulada

        return