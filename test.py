#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test.py
#  
#  Copyright 2013 Oz N <ozdeb@yenitiny>
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

# walk to table of contents and print titles and pages

import poppler

def walk_index(iterp, doc):
    while iterp.next():
      link=iterp.get_action()
      s = doc.find_dest(link.dest.named_dest)
      print link.title,' ', doc.get_page(s.page_num).get_label()
      child = iterp.get_child()
      if child:
        walk_index(child, doc)

def main():
    uri = ("file:///"+"/home/ozdeb/projects/django-pdf/pdfviewer_set/media"
            "/pdfs/2012_master_thesis.pdf")
    doc = poppler.document_new_from_file(uri, None)
      
    iterp = poppler.IndexIter(doc)
    link = iterp.get_action()
    s = doc.find_dest(link.dest.named_dest)
    print link.title,' ', doc.get_page(s.page_num).get_label()
    walk_index(iterp, doc)
    return 0
    

if __name__ == '__main__':
    main()

