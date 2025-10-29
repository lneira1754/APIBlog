from marshmallow import Schema, fields, validate

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    content = fields.Str(required=True, validate=validate.Length(min=1))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_published = fields.Bool(load_default=True)  
    author = fields.Str(dump_only=True)
    author_id = fields.Int(dump_only=True)
    categories = fields.List(fields.Int(), load_default=[]) 

class PostUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=100))
    content = fields.Str(validate=validate.Length(min=1))
    is_published = fields.Bool()
    categories = fields.List(fields.Int())