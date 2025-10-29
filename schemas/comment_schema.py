from marshmallow import Schema, fields, validate

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    text = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    created_at = fields.DateTime(dump_only=True)
    is_visible = fields.Bool(dump_only=True)
    author = fields.Str(dump_only=True)
    author_id = fields.Int(dump_only=True)
    post_id = fields.Int(required=True)