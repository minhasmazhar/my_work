from odoo import fields, api, models


class LibraryRentStage(models.Model):
    _name = 'library.rent.stage'
    _order = 'sequence,name'
    name = fields.Char()
    sequence = fields.Integer()
    fold = fields.Boolean()
    book_state = fields.Selection(
        [('available', 'Available'),
         ('borrowed', 'Borrowed'),
         ('lost', 'Lost')],
        'State', default="available")

    @api.model
    def _default_rent_stage(self):
        Stage = self.env['library.rent.stage']
        return Stage.search([], limit=1)
        stage_id = fields.Many2one(
            'library.rent.stage',
            default=_default_rent_stage
        )
