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

from __future__ import absolute_import
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from pdfviewer.models import Document

# new versions of django have:
# django.contrib.auth.decorators.staff_member_required
# consider updating !

import logging
logger = logging.getLogger(__name__)


def page_png(request, document_id, page_id=None):
   if page_id == None:
      page_id = request.GET.get("page_id", 0)
      page_id = int(page_id)
   d = get_object_or_404(Document, pk=document_id)
   p = d.get_page(int(page_id))
   return HttpResponseRedirect(p.get_absolute_url())
