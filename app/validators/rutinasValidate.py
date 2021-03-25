from marshmallow import Schema, fields, validate


class CreateRoutineSchema(Schema):
    """
    Parameters:
    -nombre String
    -descripcion String
    -intensidad String
    -categoria String

    -ejercicio List
    """

    nombre = fields.String(required=True, validate=validate.Length(
        min=1, max=45), data_key='nombre')
    descripcion = fields.String(required=True, validate=validate.Length(
        min=1, max=1000), data_key='descripcion')
    intensidad = fields.String(required=True, validate=validate.Length(
        min=1, max=45), data_key='intensidad')
    categoria = fields.String(required=True, validate=validate.OneOf(
        ['aerobico', 'anaerobico']), data_key='categoria')
    dificultad = fields.String(required=True, validate=validate.OneOf(
        ['dificil', 'facil', 'intermedio']), data_key='dificultad')

    ejercicios = fields.List(
        fields.Dict(), required=True, data_key='ejercicios')
