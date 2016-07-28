#!/usr/bin/python
# WSGI Handler sample configuration file.
#
# Change the appropriate settings below, in order to provide the parameters
# that would normally be passed in the command-line.
# (at least conf['addons_path'])
#
# For generic wsgi handlers a global application is defined.
# For uwsgi this should work:
#   $ uwsgi_python --http :9090 --pythonpath . --wsgi-file openerp-wsgi.py
#
# For gunicorn additional globals need to be defined in the Gunicorn section.
# Then the following command should run:
#   $ gunicorn openerp:service.wsgi_server.application -c openerp-wsgi.py
import os
os.environ['PYTHON_EGG_CACHE'] = "/opt/bitnami/apps/odoo/tmp/egg_cache"
import openerp

#----------------------------------------------------------
# Common
#----------------------------------------------------------
openerp.multi_process = True # Nah!

config_file = "/opt/bitnami/apps/odoo/conf/openerp-server.conf"
if not os.path.exists(config_file):
    print "Config file '%s' not found " % (config_file)
    sys.exit()
else:
    openerp.tools.config.parse_config(['-c', config_file])

# Equivalent of --load command-line option
openerp.conf.server_wide_modules = ['web']
conf = openerp.tools.config


#----------------------------------------------------------
# Generic WSGI handlers application
#----------------------------------------------------------
application = openerp.service.wsgi_server.application

conf['without_demo'] = True
conf['email_from'] = 'user@example.com'
