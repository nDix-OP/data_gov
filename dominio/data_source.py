import datetime

from odoo import fields, models, api
from .data_source_class import DataSourceClass
from .data_type import DataType
from .data_source_status import DataSourceStatus


class DataSource(models.Model):
    # nombre de la tabla de la BD (convierte . a _)
    _name = 'datagov.data.source'
    _description = 'Data source'
    _sql_constraints = [  # los check o unique
        ('name_unique', 'unique(name)', 'El atributo "Nombre" (name) debe ser único')
    ]

    # atributos mapeados
    id = fields.Id('Id', required=True)
    name = fields.Text('Name', required=True)
    steward = fields.Many2one('datagov.actor', 'Administrador', required=True)
    description = fields.Text('Descripción', required=True)
    clase = fields.Selection(selection=[  # lista valor - etiqueta
        # no veo otra forma que poner uno a uno cada valor
        # hay que meter el nombre, no deja poniendo el objeto entero
        (DataSourceClass.SERVICIO_STREAMING.name, DataSourceClass.SERVICIO_STREAMING.value),
        (DataSourceClass.SERVIDOR_BD.name, DataSourceClass.SERVIDOR_BD.value),
        (DataSourceClass.SISTEMA_FICHEROS.name, DataSourceClass.SISTEMA_FICHEROS.value),
        (DataSourceClass.SISTEMA_TRANSFERENCIA_FICHEROS.name, DataSourceClass.SISTEMA_TRANSFERENCIA_FICHEROS.value),
        (DataSourceClass.API.name, DataSourceClass.API.value),
        (DataSourceClass.NOT_A_DIGITAL_SOURCE.name, DataSourceClass.NOT_A_DIGITAL_SOURCE.value),
    ],
        string="Clase", required=True)  # en la vista no se puede modificar después
    owner = fields.Many2one('datagov.actor', 'Propietario', required=True)
    logical_model = fields.Text('Modelo lógico')
    physical_model = fields.Text('Modelo físico')
    data_type = fields.Selection(selection=[  # lista valor - etiqueta
        (DataType.STRUCTURED.name, DataType.STRUCTURED.value),
        (DataType.SEMISTRUCTURED.name, DataType.SEMISTRUCTURED.value),
        (DataType.UNSTRUCTURED.name, DataType.UNSTRUCTURED.value),
        (DataType.UNDEFINED.name, DataType.UNDEFINED.value),
    ],
        string="Tipo de datos", required=True)  # en la vista no se puede modificar después
    status = fields.Selection(selection=[  # lista valor - etiqueta
        (DataSourceStatus.ACTIVE.name, 'Activa'),
        (DataSourceStatus.PAUSED.name, 'Pausada'),
        (DataSourceStatus.INACTIVE.name, 'Inactiva'),
    ],
        string="Estado", required=True)
    statusDate = fields.Date('Fecha de estado', required=True,
                             default=datetime.date.today())  # se tiene que cambiar en onChange de status

    # al cambiar el status, la fecha de modificación es la actual
    @api.onchange("status")
    def _onchange_status_date(self):
        self.statusDate = fields.Date.today()
