"""
Clase de domino de Standard, se persiste automáticamente en la BD.
"""
from odoo import fields, models


class Procedure(models.Model):  # subclase de esta para persistir automáticamente en BD
    id = fields.Id('Id', required=True)
    name = fields.Text('Nombre', required=True)
    version = fields.Text('Versión', required=True)
    description = fields.Text('Descripción', required=True)
    owner = fields.Many2one('datagov.actor', 'Propietario', required=True)   # many2one

    # oculto, solo se ve desde política
    standard = fields.Many2many(relation='datagov_policy_standard', comodel_name='datagov.policy',
                                column1='id_standard', column2='id_policy', string='Políticas')

    # ---------------------------------------- Private Attributes ---------------------------------
    #  para la base de datos, no se muy bien que son cada una
    _name = 'datagov.standard'  # nombre de la tabla BD
    _description = 'Standard for policies'
    _order = 'id desc'  # orden del indice por defecto
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]
