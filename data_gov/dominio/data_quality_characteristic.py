from odoo import fields, models


class DataQualityCharacteristic(models.Model):
    # nombre de la tabla de la BD (convierte . a _)
    _name = 'datagov.data.quality.characteristic'
    _description = 'Data Quality Characteristic'
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    id = fields.Id('Id', required=True)
    name = fields.Text('Nombre', required=True)
    isInherent = fields.Boolean('Es inherente', required=True)
    isSystemDependent = fields.Boolean('Es dependiente del sistema', required=True)
    description = fields.Text('Descripción', required=True)
    owner = fields.Many2one('datagov.actor', 'Propietario', required=True)

    # Atributos de relaciones con otras clases del modelo
    # oculto
    dataQualityRequirement = fields.One2many('datagov.data.quality.requirement', 'dataQualityCharacteristic',
                                             string="Requisitos de calidad de datos")

    dataQualityMeasure = fields.One2many('datagov.data.quality.property.measure', 'dataQualityCharacteristic',
                                         string="Propiedad de medida de calidad de datos")
