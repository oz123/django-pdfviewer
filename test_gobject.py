#!/usr/bin/env python
# -*- coding: utf-8 -*-
# walk to table of contents and print titles and pages

import sys
from gi.repository import Poppler

def walk_index(iterp, doc):
    while iterp.next():
        link=iterp.get_action()
        dest=doc.find_dest(link.goto_dest.dest.named_dest)
        s = doc.get_page(dest.page_num-1)
        print link.goto_dest.title, dest.page_num, s.get_label()
        child = iterp.get_child()
        if child:
            walk_index(child, doc)

def main():
    uri = ("file:///"+sys.argv[1])
    doc = Poppler.Document.new_from_file(uri, None)
    iterp = Poppler.IndexIter.new(doc)
    link = iterp.get_action()
    dest=doc.find_dest(link.goto_dest.dest.named_dest)
    s = doc.get_page(dest.page_num-1)
    print link.goto_dest.title, dest.page_num, s.get_label()
    walk_index(iterp, doc)
    return 0
    

if __name__ == '__main__':
    main()


