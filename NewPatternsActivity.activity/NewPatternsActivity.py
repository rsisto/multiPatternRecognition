#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
import zipfile
import pygtk
import gtk
import pango
from sugar.activity import activity
from sugar.graphics import style
from sugar.graphics.alert import Alert

from sugar.graphics.toggletoolbutton import ToggleToolButton
from sugar.graphics.menuitem import MenuItem

from sugar.graphics import style
from sugar import network
from sugar.datastore import datastore
from sugar.graphics.alert import NotifyAlert
from gettext import gettext as _
from sugar.activity  import activityfactory

from ActivityWindows import ActivityWindows



class NewPatternsActivity(activity.Activity):
    
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        toolbox = activity.ActivityToolbox(self)
        activity_toolbar = toolbox.get_activity_toolbar()
        activity_toolbar.keep.props.visible = False
        activity_toolbar.share.props.visible = False
        self.set_toolbox(toolbox)

        toolbox.show()
        # Create the main container
        self._main_view = gtk.VBox()

        # Import our class ActivityWindows():

        # Step 1: Load class, which creates ActivityWindows.widget
        self.ActivityWindows = ActivityWindows()

        # Step 2: Remove the widget's parent
        if self.ActivityWindows.widget.parent:
            self.ActivityWindows.widget.parent.remove(self.ActivityWindows.widget)
 
        # Step 3: We attach that widget to our window
        self._main_view.pack_start(self.ActivityWindows.widget)

        # Display everything
        self.ActivityWindows.widget.show()
        self._main_view.show()
        self.set_canvas(self._main_view)
        self.show_all()


    def _destroy_cb(widget, data=None):
        Gtk.main_quit()


 
