from dacs.dac import Dac


class SpaceDac(Dac):
    def __init__(self):
        super().__init__()

    def read_type_ddl(self):
        sql = "SELECT `SType` FROM `space` group by SType"
        return self.qry_all(sql)

    def read_sid(self, stype):
        sql = "SELECT `SId` FROM `space` where `SType`=%s"
        return self.qry_all(sql, stype)

    def read_stype(self, sid):
        sql = "SELECT `SType` FROM `space` where `SId`=%s"
        return self.qry_one(sql, sid)

    def read_smoney(self, sid):
        sql = "SELECT `sPricePerHour` FROM `space` where `SId`=%s"
        return self.qry_one(sql, sid)
