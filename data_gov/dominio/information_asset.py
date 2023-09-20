from odoo import fields, models, api
from odoo.exceptions import UserError
from .category_type import CategoryType


class InformationAsset(models.Model):
    # nombre de la tabla de la BD (convierte . a _)
    _name = 'datagov.information.asset'
    _description = 'Information Asset'
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    id = fields.Id('Id', required=True)
    name = fields.Text('Nombre', required=True)
    category = fields.Many2one('datagov.category', 'Categoría', required=True)  # clase Category
    description = fields.Text('Descripción', required=True)
    securityClassification = fields.Many2one('datagov.security.classification', 'Nivel de seguridad',
                                             required=True)
    steward = fields.Many2one('datagov.actor', 'Administrador', required=True)

    # Atributos de relaciones con otras clases del modelo
    # Políticas, solo se cambian desde aquí
    policy = fields.Many2many(relation='datagov_policy_information_asset', comodel_name='datagov.policy',
                              column1='id_activo', column2='id_policy', string='Políticas')
    # atributo oculto para el requisito
    dataQualityRequirement = fields.Many2many(relation='datagov_data_quality_requirement_information_asset',
                                              comodel_name='datagov.data.quality.requirement',
                                              column1='id_data_quality_requirement', column2='id_information_asset',
                                              string='Requisitos de calidad de datos')
    dataEntities =\
        fields.Many2many(relation='datagov_data_entity_information_asset', comodel_name='datagov.data.entity',
                         column1='id_data_entity', column2='id_information_asset', string='Entidades de datos')
    dataQualityRule =\
        fields.Many2many(relation='datagov_information_asset_rule', comodel_name='datagov.data.quality.rule',
                         column1='id_activo', column2='id_regla', string='Reglas de calidad de datos')

    # restricción
    @api.onchange('category')
    def on_change_category(self):
        # comparar con el __eq__, si se pone vacío no salta pero después no deja guardar
        if self.category.type != CategoryType.INFORMATION_ASSET and self.category.name is not False:
            self.category = False  # dejar el valor anterior
            # lanzar notificación
            raise UserError("La categoría del activo de información debe ser una del tipo 'Activo de información'.")
        return

    @api.constrains('policy')
    def check_policy(self):
        if len(self.policy.ids) == 0:
            raise UserError("El activo de información debe obedecer a, al menos, una política.")

    @api.constrains('dataEntities')
    def check_data_entities(self):
        if len(self.dataEntities.ids) == 0:
            raise UserError("El activo de información debe contener, al menos, una entidad de datos.")

    @api.constrains('dataQualityRule')
    def check_data_quality_rules(self):
        if len(self.dataQualityRule.ids) == 0:
            raise UserError("El activo de información debe tener, al menos, una regla de calidad de datos.")

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
            if len(resultado) > 0 and regla.informationAsset.name != self.name:  # no incluye el actual si se borra
                texto = "La regla de calidad de datos ya está asignada a otro activo de información, entidad o " \
                        "elemento, y solo puede estar asignada a uno."
                raise UserError(texto)
