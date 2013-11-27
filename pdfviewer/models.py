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
from django.db import models
from django.db.models.signals import post_save, pre_save
import datetime
from django.conf import settings

from pyPdf import PdfFileReader
import os, os.path
import shutil, subprocess

PDF_PATH = getattr(settings, "PDF_PATH", "pdfs")
PDF_IMAGE_PATH = getattr(settings, "PDF_IMAGE_PATH", "pdfimages")

# Create your models here.
class Document(models.Model):
   pdf_file = models.FileField(upload_to=PDF_PATH)
   num_pages = models.PositiveIntegerField(blank=True, null=True)

   def get_all_pages(self):
      return [self.get_page(i) for i in xrange(0, self.num_pages)]

   def get_page(self, page_no):
      if page_no >= self.num_pages or page_no < 0:
         raise ValueError("Page number %d is out of range (0-%d)!" % (page_no, self.num_pages))
      else:
         try:
            p = self.page_set.get(page_no=page_no)
         except Page.DoesNotExist:
            p = self.load_page(page_no)
         return p
   

   def load_page(self, page_no):
      p = subprocess.Popen(["gs","-q","-dQUIET","-dPARANOIDSAFER","-dBATCH", "-dNOPAUSE",
         "-dNOPROMPT","-dMaxBitmap=500000000","-dFirstPage=%d" % (page_no+1), "-dLastPage=%d" % (page_no+1),"-dAlignToPixels=0","-dGridFitTT=0",
         "-sDEVICE=png16m","-dTextAlphaBits=4","-dGraphicsAlphaBits=4","-r144x144",
         "-sOutputFile=-", "-f%s" % os.path.join(settings.MEDIA_ROOT, self.pdf_file.name)], stdout=subprocess.PIPE)

      output_filename, fname = self._find_next_image_filename(page_no)

      try:
         os.mkdir(os.path.dirname(output_filename))
      except OSError:
         pass

      with open(output_filename, 'w') as output:
         shutil.copyfileobj(p.stdout, output)

      if p.wait() == 0: # return code 0, success
         p = Page()
         p.page_no = page_no
         p.image = fname 
         p.document = self
         p.save()
         return p
        

   def _find_next_image_filename(self, page_no):
      fillup = ""

      while True:
         fname = os.path.join(PDF_IMAGE_PATH, "document-%dp%d%s.png" % (self.id, page_no, fillup))
         output = os.path.join(settings.MEDIA_ROOT, fname)
         if not os.path.exists(output):
            break
         fillup += "_"
      return output, fname



   @staticmethod
   def pre_save_handler(sender, instance, **kwargs):
      r = PdfFileReader(instance.pdf_file)
      instance.num_pages = r.numPages

pre_save.connect(Document.pre_save_handler, sender=Document)

class Page(models.Model):
   document = models.ForeignKey("Document")
   page_no = models.PositiveIntegerField()
   image = models.ImageField(upload_to=PDF_IMAGE_PATH)

   def get_absolute_url(self):
      return self.image.url

   class Meta:
      unique_together = ("document", "page_no")
      ordering = ("page_no", "document")



