from odoo import fields, models


class DataQualityRequirement(models.Model):
    # nombre de la tabla de la BD (convierte . a _)
    _name = 'datagov.data.quality.requirement'
    _description = 'Data Quality Requirement'
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    id = fields.Id('Id', required=True)
    name = fields.Text('Nombre', required=True)
    statement = fields.Text('Definición', required=True)
    rationale = fields.Text('Justificación', required=True)
    owner = fields.Many2one('datagov.actor', 'Propietario', required=True)

    # Atributos de relaciones con otras clases del modelo
    # Activo de información
    informationAsset = fields.Many2many(relation='datagov_data_quality_requirement_information_asset',
                                        comodel_name='datagov.information.asset',
                                        column1='id_information_asset', column2='id_data_quality_requirement',
                                        string='Activos de información')
    # Data quality rule
    dataQualityRule = fields.One2many('datagov.data.quality.rule', 'dataQualityRequirement',
                                      string="Reglas de calidad de datos")
    # Data quality characteristic
    dataQualityCharacteristic = fields.Many2one('datagov.data.quality.characteristic',
                                                'Característica de calidad de datos', required=True)
