#***************************************************************************
# QGridder
# 
# Builds 2D grids for finite difference
#                             -------------------
#        begin                : 2013-04-08
#        copyright            : (C) 2013 by Pryet
#        email                : alexandre.pryet@ensegid.fr
# ***************************************************************************/
# 
#/***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************/

# CONFIGURATION
PLUGIN_UPLOAD = $(CURDIR)/plugin_upload.py

# Makefile for a PyQGIS plugin 

# translation
SOURCES = __init__.py qgridder.py ftools_utils.py \
	  qgridder_utils_base.py qgridder_utils_flopy qgridder_utils_pproc \
	  qgridder_utils_tseries \
	  qgridder_dialog_check3D.py qgridder_dialog_export qgridder_dialog_new \
	  qgridder_dialog_plot qgridder_dialog_preproc.py qgridder_dialog_refinement \
	  qgridder_dialog_settings \
	  ui_qgridder_check3D.py ui_qgridder_export.py ui_qgridder_new.py \
	  ui_qgridder_plot.py ui_qgridder_preproc.py ui_qgridder_refinement.py \
	  ui_qgridder_settings.py 

#TRANSLATIONS = i18n/gridder_en.ts
TRANSLATIONS = 

# global

PLUGINNAME = Qgridder

PY_FILES = __init__.py qgridder.py ftools_utils.py \
	  qgridder_utils_base.py qgridder_utils_flopy qgridder_utils_pproc \
	  qgridder_utils_tseries \
	  qgridder_dialog_check3D.py qgridder_dialog_export qgridder_dialog_new \
	  qgridder_dialog_plot qgridder_dialog_preproc.py qgridder_dialog_refinement \
	  qgridder_dialog_settings \


EXTRAS = icon_check3D.png icon_export.png icon_new.png \
	 icon_plot.png icon_pproc.png icon_refinement.png \
	 icon_settings.png

UI_FILES = ui_qgridder_check3D.py ui_qgridder_export.py ui_qgridder_new.py \
	  ui_qgridder_plot.py ui_qgridder_preproc.py ui_qgridder_refinement.py \
	  ui_qgridder_settings.py 
 
RESOURCE_FILES = resources.py

HELP = help/build/html

default: compile

compile: $(UI_FILES) $(RESOURCE_FILES)

%.py : %.qrc
	pyrcc5 -o $*.py  $<

%.py : %.ui
	pyuic5 -o $@ $<

%.qm : %.ts
	lrelease $<

# The deploy  target only works on unix like operating system where
# the Python plugin directory is located at:
# $HOME/.qgis2/python/plugins
deploy: compile # doc transcompile 
	mkdir -p $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)
	cp -vf $(PY_FILES) $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)
	cp -vf $(UI_FILES) $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)
	cp -vf $(RESOURCE_FILES) $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)
	cp -vf $(EXTRAS) $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)
	#cp -vfr i18n $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)
	#cp -vfr $(HELP) $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)/help

# The dclean target removes compiled python files from plugin directory
# also delets any .svn entry
dclean:
	find $(HOME)/.qgis2/python/plugins/$(PLUGINNAME) -iname "*.pyc" -delete
	find $(HOME)/.qgis2/python/plugins/$(PLUGINNAME) -iname ".svn" -prune -exec rm -Rf {} \;

# The derase deletes deployed plugin
derase:
	rm -Rf $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)

# The zip target deploys the plugin and creates a zip file with the deployed
# content. You can then upload the zip file on http://plugins.qgis2.org
zip: deploy dclean 
	rm -f $(PLUGINNAME).zip
	cd $(HOME)/.qgis2/python/plugins; zip -9r $(CURDIR)/$(PLUGINNAME).zip $(PLUGINNAME)

# Create a zip package of the plugin named $(PLUGINNAME).zip. 
# This requires use of git (your plugin development directory must be a 
# git repository).
# To use, pass a valid commit or tag as follows:
#   make package VERSION=Version_0.3.2
package: compile
		rm -f $(PLUGINNAME).zip
		git archive --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip $(VERSION)
		echo "Created package: $(PLUGINNAME).zip"

upload: zip
	$(PLUGIN_UPLOAD) $(PLUGINNAME).zip

# transup
# update .ts translation files
transup:
	pylupdate4 Makefile

# transcompile
# compile translation files into .qm binary format
transcompile: $(TRANSLATIONS:.ts=.qm)

# transclean
# deletes all .qm files
transclean:
	rm -f i18n/*.qm

clean:
	rm $(UI_FILES) $(RESOURCE_FILES)

# build documentation with sphinx
doc: 
	cd help; make html

