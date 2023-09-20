from odoo import fields, models, api
from odoo.exceptions import UserError
from .category_type import CategoryType


class Kpi(models.Model):
    # nombre de la tabla de la BD (convierte . a _)
    _name = 'datagov.kpi'
    _description = 'KPI Key Performance Indicator'
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    id = fields.Id('Id', required=True)
    name = fields.Text('Nombre', required=True)
    category = fields.Many2one('datagov.category', 'Categoría', required=True)  # clase Category
    description = fields.Text('Descripción', required=True)
    question = fields.Text('Preguntas a las que responde', required=True)
    calculation = fields.Text('Cálculo', required=True)
    interpretation = fields.Text('Interpretación', required=True)
    collectedBy = fields.Many2one('datagov.actor', 'Recogido por', required=True)
    frequencyOfCollection = fields.Text('Frecuencia de recogida', required=True)
    disseminationMode = fields.Text('Modo de difusión', required=True)
    frequencyOfDissemination = fields.Text('Frecuencia de difusión', required=True)
    disseminatedBy = fields.Many2one('datagov.actor', 'Difundido por', required=True)
    # Lista de a los que se difunde
    disseminatedTo = fields.Many2many(relation='datagov_kpi_disseminated_to', comodel_name='datagov.actor',
                                      column1='id_kpi', column2='id_actor', string='Difundido a')
    owner = fields.Many2one('datagov.actor', 'Propietario', required=True)

    # Atributos de relaciones con otras clases del modelo
    objective = fields.Many2one('datagov.dg.objective', 'Objetivo')  # puede ser nulo
    # solo se ve desde el activo de información
    inputParameter = fields.Many2many(relation='datagov_kpi_input_parameter', comodel_name='datagov.input.parameter',
                                      column1='id_kpi', column2='id_parameter', string='Parámetros de entrada')

    policy = fields.Many2many(relation='datagov_policy_kpi', comodel_name='datagov.policy',
                              column1='id_kpi', column2='id_policy', string='Políticas')

    # restricción
    @api.onchange('category')
    def on_change_category(self):
        # comparar con el __eq__, si se pone vacío no salta pero después no deja guardar
        if self.category.type != CategoryType.KPI and self.category.name is not False:
            self.category = False  # dejar el valor anterior
            # mensaje distinto dependiendo de lo que se quiera hacer
            if self.category.name == 'Medida de calidad de datos':
                texto = "Si desea convertir un KPI en uno de calidad de datos, debe borrar este y crear uno nuevo " \
                        'desde la vista "Indicadores de calidad de datos (KPIs)"'
            else:
                # lanzar notificación
                texto = "La categoría del KPI debe ser una del tipo 'KPI',y tampoco la medida de calidad de datos ."
            raise UserError(texto)
        return

    @api.constrains('inputParameter')
    def check_has_input_parameter(self):
        if len(self.inputParameter.ids) == 0:
            raise UserError("La métrica debe tener, al menos, un parámetro de entrada.")
