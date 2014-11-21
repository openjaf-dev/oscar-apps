from django.conf import settings
import odoorpc


def create_database_in_backend(user):
    db_name = 'backend_%s' % user.username
    odoo = odoorpc.ODOO(settings.ODOO_SERVER, 'jsonrpc', 8069)
    odoo.config['timeout'] = 600
    odoo.db.create('admin', db_name, demo=False,
                   lang='en_US', admin_password='admin')

    odoo.login(db_name)
    mid = odoo.execute('ir.module.module', 'search',
                       [('name', '=', 'oe_reserva_markets')])
    if mid:
        # 1. Install Reserva addon for Odoo
        odoo.execute('ir.module.module', 'button_immediate_install', mid)

        # 2. Update user with permissions for sales
        vals = {'name': user.first_name, 'login': user.email}
        user_id = odoo.execute('res.users', 'create', vals)
        res = odoo.execute('res.users', 'read', user_id, ['groups_id'])
        gids = odoo.execute('res.groups', 'search',
                           [('name', '=', 'Manager'),
                            ('category_id.name', '=', 'Sales')])
        group_ids = res['groups_id'] + gids
        odoo.execute('res.users', 'write', user_id,
                     {'groups_id': [(6, 0, group_ids)],
                      'password': 'admin'})

        # 3. Update company name with user organization
        company_id = odoo.execute('res.company', 'search', [])
        if company_id:
            odoo.execute('res.company', 'write', company_id[0],
                         {'name': user.organization})


def login_in_backend(user):
    db_name = 'backend_%s' % user.username
    args = (settings.ODOO_SERVER, db_name, user.email, 'admin')
    return 'http://%s:8069/login?db=%s&login=%s&key=%s' % args
