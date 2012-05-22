import zipfile

class Zipper:

  def __init__(self, file, mode = "w", compression = zipfile.ZIP_DEFLATED, allowZip64=False):

    self.__zipFile = zipfile.ZipFile(file, mode, compression, allowZip64)

  def write(self, writeDataSet = None, writeStrDataSet = None):

    if writeDataSet:
      dataSet = writeDataSet.getDataSet()
      for writeData in dataSet:

        self.__zipFile.write(
          writeData.getFileUri(),
          writeData.getArchiveUri(),
          writeData.getCompressType()
        )

    if writeStrDataSet:
      dataSet = writeStrDataSet.getDataSet()
      for writeStrData in dataSet:

        self.__zipFile.writestr(
          writeStrData.getZipInfo(),
          writeStrData.getBytes()
        )

  def close(self):
    self.__zipFile.close()

class WriteDataSet:

  def __init__(self):
    self.__dataSet = []

  def add(self, fileUri, archiveUri=None, compressType=None):
    self.__dataSet.append(WriteData(fileUri, archiveUri, compressType))

  def getDataSet(self):
    return self.__dataSet


class WriteData:

  def __init__(self, fileUri, archiveUri=None, compressType=None):

    self.__fileUri = fileUri
    self.__archiveUri = archiveUri
    self.__compressType = compressType

  def getFileUri(self):
    return self.__fileUri

  def getArchiveUri(self):
    return self.__archiveUri

  def getCompressType(self):
    return self.__compressType


class WriteStrDataSet:

  def __init__(self):
    self.__dataSet = []

  def add(self, bytes, zipInfo):
    self.__dataSet.append(WriteStrData(bytes, zipInfo))

  def getDataSet(self):
    return self.__dataSet

class WriteStrData:

  def __init__(self, bytes, zipInfo):

    self.__zipInfo = zipInfo
    self.__bytes = bytes

  def getZipInfo(self):
    return self.__zipInfo

  def getBytes(self):
    return self.__bytes


def createBytesFile():

  import StringIO
  return StringIO.StringIO()

def createZipInfoOfNowTime(archiveUri):

  import datetime
  date = datetime.datetime.now()

  return zipfile.ZipInfo(archiveUri, date.timetuple()[:6])

def output(response, file, fileName):

  response.headers["Content-Type"] = "application/zip"
  response.headers['Content-Disposition'] = "attachment; filename=" + fileName + ".zip"
  response.out.write(file.getvalue())
