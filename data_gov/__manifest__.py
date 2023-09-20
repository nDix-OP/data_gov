# -*- coding: utf-8 -*-
# More info at https://www.odoo.com/documentation/master/reference/module.html

{
    "name": "Gobernanza de datos",
    "author": "Iván Ortiz del Noval",
    "category": 'Data/Technical',
    "depends": [
        "base",
        "web"
    ],
    "description": "Herramienta para la definición de un marco de gobernanza de datos dentro de la compañía.",
    "data": [
        # rellenar con archivos, los csv o xml, ...
        "datos/datagov_datos_iniciales.xml",  # cargar datos iniciales
        "seguridad/ir.model.access.csv",  # permisos del modelo de dominio
        "vistas/datagov_categorias_views.xml",
        "vistas/datagov_actores_views.xml",
        "vistas/datagov_roles_views.xml",
        "vistas/datagov_data_sources_views.xml",
        "vistas/datagov_dgobjectives_views.xml",
        "vistas/datagov_ubicaciones_views.xml",
        "vistas/datagov_unidades_org_views.xml",
        "vistas/datagov_terminos_glosario_views.xml",
        "vistas/datagov_procedimientos_views.xml",
        "vistas/datagov_principios_views.xml",
        "vistas/datagov_reglas_calidad_datos_views.xml",
        "vistas/datagov_estandares_views.xml",
        "vistas/datagov_parametros_views.xml",
        "vistas/datagov_clasificacion_seguridad_views.xml",
        "vistas/datagov_entidades_datos_views.xml",
        "vistas/datagov_elementos_datos_views.xml",
        "vistas/datagov_activos_informacion_views.xml",
        "vistas/datagov_politicas_views.xml",
        "vistas/datagov_kpi_views.xml",
        "vistas/datagov_caracteristica_calidad_datos_views.xml",
        "vistas/datagov_requisitos_calidad_datos_views.xml",
        "vistas/datagov_medidas_calidad_datos_views.xml",
        "vistas/datagov_main_menu.xml",  # IMPORTANTE: ponerlo al final porque usa cosas de los otros xml de vistas
        "static/description/icon.png",  # Logo
    ],
    "application": True,
    "license": "LGPL-3",
    "version": "1.0",
    "price": 0.00,
    "currency": "EUR",
    "support": "marta.zorrilla@unican.es"  # opcional
}
