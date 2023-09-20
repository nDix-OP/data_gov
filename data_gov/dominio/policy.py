import datetime

from odoo import fields, models, api
from odoo.exceptions import UserError
from .category_type import CategoryType
from .status import Status as St


class InformationAsset(models.Model):
    # nombre de la tabla de la BD (convierte . a _)
    _name = 'datagov.policy'
    _description = 'Policy'
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    id = fields.Id('Id', required=True)
    name = fields.Text('Nombre', required=True)
    status = fields.Selection(selection=[  # lista valor - etiqueta
        (St.CURRENT.name, 'Vigente'),
        (St.NOT_IN_FORCE.name, 'Retirado'),
        (St.PROPOSED.name, 'Propuesto')
    ], string='Estado', required=True)
    category = fields.Many2one('datagov.category', 'Categoría', required=True)  # clase Category
    statusDate = fields.Date('Fecha de estado', required=True,
                             default=datetime.date.today())  # se tiene que cambiar en onChange de status
    scope = fields.Text('Alcance', required=True)
    statement = fields.Text('Definición', required=True)
    rationale = fields.Text('Justificación', required=True)
    implication = fields.Text('Implicaciones', required=True)
    owner = fields.Many2one('datagov.actor', 'Propietario', required=True)

    # Atributos de relaciones con otras clases del modelo
    procedure = fields.Many2many(relation='datagov_policy_procedure', comodel_name='datagov.procedure',
                                 column1='id_policy', column2='id_procedure', string='Procedimientos')
    standard = fields.Many2many(relation='datagov_policy_standard', comodel_name='datagov.standard',
                                column1='id_policy', column2='id_standard', string='Estándares')
    metric = fields.Many2many(relation='datagov_policy_kpi', comodel_name='datagov.kpi',
                              column1='id_policy', column2='id_kpi', string='KPIs asociados')
    dataQualityMetric = fields.Many2many(relation='datagov_policy_property_measure',
                                         comodel_name='datagov.data.quality.property.measure',
                                         column2='id_property_measure', column1='id_policy',
                                         string='KPIs de calidad de datos asociados')
    # solo se ve desde el activo de información
    informationAsset =\
        fields.Many2many(relation='datagov_policy_information_asset', comodel_name='datagov.information.asset',
                         column1='id_policy', column2='id_activo', string='Activos de información')

    # restricción
    @api.onchange('category')
    def on_change_category(self):
        # comparar con el __eq__, si se pone vacío no salta pero después no deja guardar
        if self.category.type != CategoryType.POLICY and self.category.name is not False:
            self.category = False  # dejar el valor anterior
            # lanzar notificación
            raise UserError("La categoría de la política debe ser una del tipo 'Política'.")
        return

    # al cambiar el status, la fecha de modificación es la actual
    @api.onchange("status")
    def _onchange_status_date(self):
        self.statusDate = fields.Date.today()
