{
    'name': "My library",
    'summary': "Manage books easily",
    'description': """
Manage Library
==============
Description related to library.
""",
    'author': "Minhas",
    'website': "http://www.example.com",
    'category': 'Uncategorized',
    'version': '13.0.1',
    'depends': ['base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/library_book.xml',
        'views/library_member.xml',
        'views/library_book_categ.xml',
        'views/library_stage.xml',
    ],
    'demo': ['demo.xml'],
    'application': True,
    'sequence': 1,
    'installable': True,
}
