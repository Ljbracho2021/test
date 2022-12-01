
from odoo import api, fields, models

class BecaIndice(models.Model):
    _name        = 'beca.indice'
    _description = 'Gestión de Becas - indice'
    _rec_name    = 'numero'

       
    numero       = fields.Char(index=True, string='Número Planilla', required = True)
    cedula       = fields.Char(string='Cédula de Identidad', required = True)
