# -*- coding: utf-8 -*-

from email.policy import default
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class BecaCarrera(models.Model):
    _name        = 'beca.carrera'
    _description = 'Gestión beca - carrera'
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

    oferta_line_ids = fields.One2many('carrera.oferta', 'carrera_id', string="Universidades")

    @api.constrains('nombre')
    def check_nombre(self):
        for rec in self:
            carrera = self.env['beca.carrera'].search([('nombre', '=', rec.nombre), ('id', '!=', rec.id)])
            if carrera:
                raise ValidationError(_("Nombre %s Ya Existe" % rec.nombre))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('beca.carrera') or _('New')
        res = super(BecaCarrera, self).create(vals)
        return res

    @api.onchange('nombre')
    def _onchange_nombre(self):
         
        if self.nombre:
            self.nombre = self.nombre.upper()
        
        domain = [('nombre', '=', self.nombre)]
        if self.id.origin:
            domain.append(('id', '!=', self.id.origin))
        
        if self.env['beca.carrera'].search(domain, limit=1):
            return {'warning': {
                'title': ("Precauciòn:"), 
                'message': ("El nombre para la unidad de producción ya existe ", self.nombre), 
            }}

class CarreraOferta(models.Model):
    _name = "carrera.oferta"
    _description = "Carreras / Oferta Academica"

    
    universidad_id = fields.Many2one('beca.universidad', string="Universidad", required = True)
    
    carrera_id = fields.Many2one('beca.carrera', string="Carrera")

