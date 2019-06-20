#coding:utf-8

class _const:
  class ConstError(TypeError): pass
  class ConstCaseError(ConstError): pass

  def __setattr__(self, name, value):
      if name in self.__dict__:
          raise self.ConstError("can't change const %s" % name)
      if not name.isupper():
          raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
      self.__dict__[name] = value

######## 日志
log = _const()
log.LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
log.DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
log.LOG_FILE = '/Users/leslie/MyProjects/Data/Okooo/okparse.log'



######## URL
my_const = _const()
# 澳客单场url
my_const.MATCH_URL_PRE = "http://www.okooo.com/danchang/"
# 欧赔页面通过 ajax 获取博彩公司赔率.
my_const.ODDS_EMBEDED_TEMPLATE_URL = "http://www.okooo.com/soccer/match/{matchId}/odds/ajax/?page={pageNum}&trnum=30&companytype=BaijiaBooks&type=0";


######## 文件
# 保存下载的文件
my_const.LOCAL_DATA_DIR = "/Users/leslie/MyProjects/Data/Okooo/";
# match 文件, 即单场页面的数据.
my_const.MATCH_HTML = "match.html"
my_const.MATCH_DAT = "match.dat"
# 博彩公司编号文件
my_const.CORP_NO_FILE = "corpNo.dat"
# 欧赔目录, 保存初赔文件等.
my_const.EURO_ODDS_DIR = "euroOdds"
# 初赔目录
my_const.EURO_ODDS_FIRST_DIR = "firstEuroOdds"
