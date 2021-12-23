from odoo import models, fields, api
from datetime import timedelta, datetime
from odoo.exceptions import UserError
from odoo.tools.translate import _
from lxml import etree

# Abstract Model
from odoo14.src.odoo14.odoo.odoo import exceptions
from odoo14.src.odoo14.odoo.odoo.cli.scaffold import env


class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active


class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = ['base.archive']
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'name'
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)',
         'Book title must be unique.'),
        ('positive_page', 'CHECK(pages>0)',
         'No of pages must be positive')
    ]

    author_ids = fields.Many2many('res.partner', string='Authors')
    name = fields.Char('Title', required=True)
    short_name = fields.Char('Short Title')
    notes = fields.Text('Internal Notes')
    state = fields.Selection([
        ('draft', 'Unavailable'), ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost')],
        'State', default="draft")

    @api.model
    def is_allowed_transition(self, old_state, new_state):

        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                raise UserError(_('Moving from %s to %s is not allowed') % (book.state, new_state))

    def make_available(self):
        self.change_state('available')

    def make_borrowed(self):
        self.change_state('borrowed')

    def make_lost(self):
        self.change_state('lost')

    description = fields.Html('Description')
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')

    def change_release_date(self):
        self.ensure_one()
        self.date_release = fields.Date.today()

    date_updated = fields.Datetime('Last Updated')
    pages = fields.Integer('Number of Pages')
    reader_rating = fields.Float(
        'Reader Average Rating',
        digits=(14, 4),  # Optional precision decimals,
    )
    cost_price = fields.Float(
        'Book Cost', digits='Book Price')
    currency_id = fields.Many2one(
        'res.currency', string='Currency')
    retail_price = fields.Monetary(
        'Retail Price',
        # optional: currency_field='currency_id',
    )
    publisher_id = fields.Many2one(
        'res.partner', string='Publisher',
        # optional:
        ondelete='set null',
        context={},
        domain=[],
    )
    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_age',
        inverse='_inverse_age',
        search='_search_age',
        store=True,
        # optional
        compute_sudo=True  # optional
    )
    category_id = fields.Many2one('library.book.category')
    publisher_id = fields.Many2one(
        'res.partner', string='Publisher')
    publisher_city = fields.Char(
        'Publisher City',
        related='publisher_id.city',
        readonly=True)
    ref_doc_id = fields.Reference(
        selection='_referencable_models',
        string='Reference Document')

    # ======================= ORM METHODS (START)=====================================

    @api.model  # _create_multi
    def create(self, values):
        print("Create function overridden!")
        result = super(LibraryBook, self).create(values)
        print(values)
        return result

    # @api.model 
    def write(self, values):
        result = super(LibraryBook, self).write(values)
        print(values)
        print(result)
        return result

    # @api.model
    def copy(self, default=None):
        print("copy function overridden!")
        # raise exceptions.UserError(_('You cannot duplicate the doctor record.'))
        if default is None:
            default = {}
        if not default.get('name'):
            print(default.get('name'))
            default['name'] = _("%s (copy)", self.name)
        return super(LibraryBook, self).copy(default)

    def unlink(self):

        # print("self values ", self)
        for rec in self:
            if self.age_days > 0:
                raise UserError(_('You cannot delete this record.'))
        rtn = super(LibraryBook, self).unlink()
        # print(rtn)
        return rtn

    def default_get(self, fields):
        print("Default get method override in Library Book")
        rtn = super(LibraryBook, self).default_get(fields)
        print(str(datetime.today()))
        # obj_list = self.env['hospital.doctor'].search(
        #     ['|', ('doctor_name', 'ilike', 'sami'),
        #      ('doctor_name', 'ilike', 'osama')])
        # obj_list = self.env['hospital.doctor'].search([]).read(['id', 'doctor_name', 'age'])
        # obj_list = self.env['hospital.doctor'].browse([1, 3, 5])
        # for stud in obj_list:
        # obj_list = self.env['hospital.doctor'].search([]).get_metadata()
        # obj_list = self.env['hospital.doctor'].fields_get()
        # obj_list = self.env['hospital.doctor'].fields_get(['field names',''], ['attributes',''])
        # obj_list = self.env['hospital.doctor'].fields_get([], ['type', 'string'])
        # obj_list = self.env['hospital.doctor'].read_group([], fields=['gender'], groupby=['gender'])
        # obj_list = self.env['hospital.doctor'].search([]).filtered(lambda x: x.gender == 'male')
        # for rec in obj_list:
        #     print(rec.doctor_name)
        # print(type(obj_list))
        # print(obj_list)
        # domain = [('email', 'not in', [False, None])]
        # records = self.env['hospital.doctor'].search([])
        # email_list = records.mapped('doctor_name')
        # print(email_list)
        # for rec in email_list:
        #     print(rec)
        obj_list = self.env['hospital.doctor'].search([]).sorted(lambda x: x.id)

        query = '''SELECT * FROM
        res_partner'''
        self.env.cr.execute(query)
        print(self.env.cr.fetchall())

        print(type(obj_list))
        print(obj_list)
        # print(type(env.cr.dbname))
        rtn['date_release'] = datetime.today()
        return rtn

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        # print("View_id ", view_id)
        # print("view_type ", view_type)
        # print("toolbar ", toolbar)
        # print("submenu ", submenu)

        res = super(LibraryBook, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                       submenu=submenu)
        # if view_type == 'form':
        #     doc = etree.XML(res['arch'])
        # name_field = doc.xpath("//field[@name='name']")
        # if name_field:
        #     name_field[0].addnext(
        #         etree.Element('label', {'string': 'Hello this is custom label (fields_view_get method)'}))
        #     res['arch'] = etree.tostring(doc, encoding='unicode')

        #     author_field = doc.xpath("//field[@name='author_ids']")
        #     print(author_field)
        #     if author_field:
        #         author_field[0].set("string", "Author (Fields_view_get method)")
        #     res['arch'] = etree.tostring(doc, encoding='unicode')
        # if view_type == 'tree':
        #     doc = etree.XML(res['arch'])
        #     pages_field = doc.xpath("//field[@name='pages']")
        #     if pages_field:
        #         pages_field[0].addnext(
        #             etree.Element('field', {'string': 'Pages (fields_view_get method)', 'name': 'pages'}))
        #     res['arch'] = etree.tostring(doc, encoding='unicode')

        return res

    # ======================= ORM METHODS (END)=====================================
    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                # print(str(fields.Date.today()))
                raise models.ValidationError('Release date must be in the past.')

    @api.depends('date_release')
    def _compute_age(self):
        today = fields.Date.today()
        for book in self:
            if book.date_release:
                delta = today - book.date_release
                book.age_days = delta.days
            else:
                book.age_days = 0

    def _inverse_age(self):
        today = fields.Date.today()

        for book in self.filtered('date_release'):
            d = today - timedelta(days=book.age_days)
            book.date_release = d

    def _search_age(self, operator, value):
        today = fields.Date.today()

        value_days = timedelta(days=value)
        value_date = today - value_days
        # convert the operator:
        # book with age > value have a date < value_date
        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]

    def name_get(self):
        result = []

        for record in self:
            rec_name = "%s (%s)" % (record.name, record.date_release)
            result.append((record.id, rec_name))
        return result

    def log_all_library_members(self):

        # This is an empty recordset of model library.member
        library_member_model = self.env['library.member'].search([])
        print("ALL MEMBERS:", library_member_model)
        return True


# class inheritance
class ResPartner(models.Model):
    _inherit = 'res.partner'

    published_book_ids = fields.One2many('library.book', 'publisher_id', string='Published Books')
    authored_book_ids = fields.Many2many('library.book', string='Authored Books')
    count_books = fields.Integer('Number of Authored Books', compute='_compute_count_books')

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)


# Delegation Inheritance
class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    partner_id = fields.Many2one(
        'res.partner',
        ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')
