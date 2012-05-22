#!-*- coding:utf-8 -*-
import logging

from google.appengine.ext import webapp

from util import *
from zipper import *

SPEED = 500

class Download(webapp.RequestHandler):
    def get(self):
        if self.request.get('url'):
            url = self.request.get('url')
        else:
            url = "http://www.aozora.gr.jp/cards/000879/files/16_ruby_344.zip"
        if self.request.get('speed'):
            speed = int(self.request.get('speed'))
        else:
            speed = SPEED
        if self.request.get('maxmin'):
            maxMin = int(self.request.get('maxmin'))
        if self.request.get('type'):
            type = self.request.get('type')
        else:
            type = "zip"

        txt = UtilNetwork.downloadAozoraZip(url)
        txt = txt.decode("shift_jis")
        txt = self.addAnnotationTitle(txt, speed)
        txt = self.addAnnotationBefore(txt, speed)
        if self.request.get('maxmin'):
            txt = self.addAnnotationAfter(txt, speed, maxMin)
        txt = txt.encode('utf-8')

        outputName = url.rsplit('/', 1)[1].split('.')[0]
        if type == "txt":
            self.response.out.write(txt)
        else:
            self.outputByZip(self, txt, outputName)

    @staticmethod
    def addAnnotationTitle(txt, speed):
        index = txt.index('\r\n')
        s = u"　☆読了時間：%d分☆" % (Download.calculateMins(len(txt), speed))
        return txt[:index] + s + txt[index:]

    @staticmethod

    def addAnnotationBefore(txt, speed):
        ret = ""
        txts = txt.split('\r\n\r\n')
        for t in txts:
            if len(t) > 500:
                s = u"☆読了時間：%d分 文字数：%d☆\r\n" % (Download.calculateMins(len(t), speed), len(t))
                t = s + t
            ret += t + "\r\n\r\n"
        return ret

    @staticmethod
    def addAnnotationAfter(txt, speed, maxMin):
        ret = ""
        sum = 0
        txts = txt.split('\r\n\r\n')
        for t in txts:
            sum += Download.calculateMins(len(t), speed)
            if sum > maxMin:
                t += u"\r\n☆%d分経過しました☆\r\n" % (maxMin)
                sum = 0
            ret += t + "\r\n\r\n"
        return ret

    @staticmethod
    def calculateMins(cnt, speed):
        return int(round(float(cnt) / float(speed)))

    @staticmethod
    def outputByZip(self, txt, outputName):
        # 出力用ファイル作成
        fileName = txt.split('\r\n')[0]
        f = createBytesFile()
        writeDataSet = WriteDataSet()
        writeStrDataSet = WriteStrDataSet()
        writeStrDataSet.add(txt, createZipInfoOfNowTime(fileName + ".txt"))
        zipper = Zipper(f)
        zipper.write(writeDataSet, writeStrDataSet)
        zipper.close()

        output(self.response, f, outputName)
