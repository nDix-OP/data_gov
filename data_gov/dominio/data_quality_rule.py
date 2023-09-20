from odoo import fields, models, api
from odoo.exceptions import UserError


class DataQualityRule(models.Model):
    # nombre de la tabla de la BD (convierte . a _)
    _name = 'datagov.data.quality.rule'
    _description = 'Data Quality Rule'
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    # atributos mapeados
    id = fields.Id('Id', required=True)
    name = fields.Text('Nombre', required=True)
    description = fields.Text('Descripción', required=True)
    owner = fields.Many2one('datagov.actor', 'Propietario', required=True)   # many2one (tabla BD, descripción)

    # los Many2One que hay que poner como many2many para que se puedan escoger desde las otras clases
    # solo uno puede ser no nulo a la vez, y solo un valor
    dataElement = fields.Many2many(relation='datagov_data_element_rule', comodel_name='datagov.data.element',
                                   column1='id_regla', column2='id_elemento', string='Elemento de datos que la aplica')
    dataEntity = fields.Many2many(relation='datagov_data_entity_rule', comodel_name='datagov.data.entity',
                                  column1='id_regla', column2='id_entidad', string='Entidad de datos que la aplica')
    informationAsset =\
        fields.Many2many(relation='datagov_information_asset_rule', comodel_name='datagov.information.asset',
                         column1='id_regla', column2='id_activo', string='Activo de información que la aplica')

    dataQualityRequirement = fields.Many2one('datagov.data.quality.requirement', 'Requisito de calidad de datos',
                                             required=True)
