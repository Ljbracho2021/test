# -*- coding: utf-8 -*-

from email.policy import default
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class BecaUniversidad(models.Model):
    _name        = 'beca.universidad'
    _description = 'Gestión beca - universidad'
    _rec_name    = 'nombre'
    _order       = 'nombre'

    name = fields.Char(string='Nro.', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))   

    nombre = fields.Char('Nombre', required = True)

    image = fields.Image(max_width=100, max_height=100, store=True)
   
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Favorito'),
    ], required=True, default='0', tracking=True)

    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the product without removing it.")
    note = fields.Text(string="Observaciones")

    sede_line_ids = fields.One2many('universidad.sedes', 'universidad_id', string="Sedes")

    @api.constrains('nombre')
    def check_nombre(self):
        for rec in self:
            universidad = self.env['beca.universidad'].search([('nombre', '=', rec.nombre), ('id', '!=', rec.id)])
            if universidad:
                raise ValidationError(_("Nombre %s Ya Existe" % rec.nombre))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('beca.universidad') or _('New')
        res = super(BecaUniversidad, self).create(vals)
        return res

    @api.onchange('nombre')
    def _onchange_nombre(self):
         
        if self.nombre:
            self.nombre = self.nombre.upper()
        
        domain = [('nombre', '=', self.nombre)]
        if self.id.origin:
            domain.append(('id', '!=', self.id.origin))
        
        if self.env['beca.universidad'].search(domain, limit=1):
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("El nombre para la unidad de producción ya existe ", self.nombre), 
            }}

class UniversidadSedes(models.Model):
    _name = "universidad.sedes"
    _description = "AccionGobierno / Accion Lines"

    nombre_sede = fields.Char(string='Nombre', store=True, required=True)

    universidad_id = fields.Many2one('beca.universidad', string="Universidad")
