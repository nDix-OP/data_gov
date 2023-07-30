from odoo import fields, models, api
from odoo.exceptions import UserError


class DataElement(models.Model):
    # nombre de la tabla de la BD (convierte . a _)
    _name = 'datagov.data.element'
    _description = 'Data Element'
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    id = fields.Id('Id', required=True)
    name = fields.Text('Nombre', required=True)
    conceptualDomain = fields.Text('Dominio conceptual', required=True)
    valueDomain = fields.Text('Valor del dominio', required=True)

    # Atributos de relaciones con otras clases del modelo
    term = fields.Many2one('datagov.glossary.term', 'Término del glosario', ondelete='set null')
    dataQualityRule = \
        fields.Many2many(relation='datagov_data_element_rule', comodel_name='datagov.data.quality.rule',
                         column1='id_elemento', column2='id_regla', string='Reglas de calidad de datos')
    # Hacer la composición con DataElement
    dataEntity = fields.Many2one('datagov.data.entity', 'Entidad  de datos que compone', required=True)

    @api.onchange('dataQualityRule')
    def onchange_data_quality_rule(self):
        lista = self.dataQualityRule.ids
        for i in lista:
            # más cómodo si se ejecuta la query conjunta
            query = "SELECT id_regla, id_elemento FROM datagov_data_element_rule WHERE id_regla = " + str(i) + \
                    " UNION SELECT id_regla, id_entidad FROM datagov_data_entity_rule WHERE id_regla = " + str(i) + \
                    " UNION SELECT id_regla, id_activo FROM datagov_information_asset_rule WHERE id_regla = " + str(i)
            self.env.cr.execute(query)
            resultado = self.env.cr.fetchall()
            regla = self.env['datagov.data.quality.rule'].browse(i)
            if len(resultado) > 0 and regla.dataElement.name != self.name:  # no incluye el actual si se borra
                texto = "La regla de calidad de datos ya está asignada a otro activo de información, entidad o " \
                        "elemento, y solo puede estar asignada a uno."
                raise UserError(texto)
