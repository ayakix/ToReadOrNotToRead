#!-*- coding:utf-8 -*-
import logging
import urllib
import urllib2
import zipfile
import tempfile

class UtilNetwork():
    @staticmethod
    def downloadAozoraText(url):
        o = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
        f = o.open(url)
        return f.read()

    @staticmethod
    def downloadAozoraZip(url):
        o = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
        f = o.open(url)
        return UtilZip.unzip(f)

class UtilZip():
    @staticmethod
    def unzip(f):
        temp = tempfile.TemporaryFile()
        temp.write(f.read())
        zf = zipfile.ZipFile(temp, 'r')
        data = None
        for fileName in zf.namelist():
            if fileName.find(".txt") != -1:
                data = zf.read(fileName)
                break;
        zf.close()
        return data
