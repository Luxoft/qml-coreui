TEMPLATE = subdirs

SUBDIRS += lib_coreui
SUBDIRS += plugin_coreui

SUBDIRS += lib_sql
SUBDIRS += plugin_sql

SUBDIRS += lib_json
SUBDIRS += plugin_json

SUBDIRS +=  lib_trace
SUBDIRS +=  plugin_trace

SUBDIRS +=  lib_shell
SUBDIRS +=  plugin_shell


SUBDIRS +=  lib_http
SUBDIRS +=  plugin_http

plugin_coreui.depends += lib_coreui
plugin_sql.depends += lib_sql
plugin_json.depends += lib_json
plugin_trace.depends += lib_trace
plugin_shell.depends += lib_shell
plugin_shell.depends += lib_coreui
plugin_http.depends += lib_http
