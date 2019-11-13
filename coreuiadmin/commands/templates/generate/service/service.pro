TEMPLATE = subdirs

SUBDIRS += frontend
SUBDIRS += plugin
SUBDIRS += backend
SUBDIRS += backend_simu
SUBDIRS += backend_qtro
SUBDIRS += server_qtro

plugin.depends = frontend
backend.depends = frontend
backend_simu.depends = frontend
backend_qtro.depends = frontend
server_qtro.depends = frontend