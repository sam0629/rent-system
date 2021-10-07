from dacs.dac import Dac


class TradeDac(Dac):
    def __init__(self):
        super().__init__()

    def writetrade(self,uid,sid,trade_date):
        sql = '''insert into `trade` (`UId`,`SId`,`TradeTime`) values (%s,%s,%s) '''
        self.exec_cmd(sql,(uid,sid,trade_date))

    def qry_times(self,uid):
        sql = '''SELECT `SId`,`TradeTime` FROM `trade` where `UId` = %s'''
        return self.qry_all(sql,uid)
    def qry_tid(self,trade_time,sid,uid):
        sql = '''
        SELECT `TId` FROM `trade` 
        where `UId` = %s and `TradeTime` = %s and `SID` = %s 
        '''
        return self.qry_one(sql,(uid,trade_time,sid))

