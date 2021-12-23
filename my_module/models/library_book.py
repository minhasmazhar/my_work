from odoo import models, api, fields


class LibraryBook(models.Model):
    _name = 'library.book'
    _rec_name = 'name'
    author_ids = fields.Many2many('res.partner', string='Authors')
    name = fields.Char('Title', required=True)
    short_name = fields.Char('Short Title')
    notes = fields.Text('Internal Notes')
    state = fields.Selection([
        ('draft', 'Unavailable'), ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost')],
        'State', default="draft")
    description = fields.Html('Description')
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')
