# -*- coding: utf-8 -*-
#
#  Copyright 2013 Oz Nahum <nahumoz@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from __future__ import absolute_import
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',

    # #########################################################################
    # the common stuff
    # #########################################################################
    # the admin and developer documentation
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # the admin interface
    url(r'^admin/', include(admin.site.urls)),
    url("^(?P<document_id>\d+).png$", "pdfviewer.views.page_png"),
    url("^(?P<document_id>\d+)p(?P<page_id>\d+).png$", "pdfviewer.views.page_png"),

    # view tpa list
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
