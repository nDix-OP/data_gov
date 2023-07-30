# . significa directorio actual
# aquí van todos los import, poner from . import <cada archivo de la carpeta>

# este paquete es para las clases de dominio, las del modelo de dominio, ir añadiendo mientras se creen
from . import category_type, role, category, data_type, actor, data_source, data_source_class, data_quality_rule, \
    glossary_term, status, location, organization_unit, dg_objective, procedure, principle, standard, input_parameter, \
    security_classification, data_entity, data_element, information_asset, policy, kpi, data_quality_characteristic, \
    data_quality_requirement, data_quality_property_measure
