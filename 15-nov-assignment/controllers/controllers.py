# -*- coding: utf-8 -*-
# from odoo import http


# class 15-nov-assignment(http.Controller):
#     @http.route('/15-nov-assignment/15-nov-assignment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/15-nov-assignment/15-nov-assignment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('15-nov-assignment.listing', {
#             'root': '/15-nov-assignment/15-nov-assignment',
#             'objects': http.request.env['15-nov-assignment.15-nov-assignment'].search([]),
#         })

#     @http.route('/15-nov-assignment/15-nov-assignment/objects/<model("15-nov-assignment.15-nov-assignment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('15-nov-assignment.object', {
#             'object': obj
#         })
