@echo off
set PATH=/opt/bitnami/python/scripts;/opt/bitnami/python;%PATH%
set PYTHONPATH=/opt/bitnami/python/Lib/site-packages;/opt/bitnami/apps/odoo/Lib/site-packages;
/opt/bitnami/python/python.exe "/opt/bitnami/apps/odoo/Scripts/openerp-server" %*
            