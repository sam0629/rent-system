from dacs.dac import Dac


class RecordDac(Dac):
    def __init__(self):
        super().__init__()
    def write_record(self,pid,tid,amoumt,saleprice):
        sql = '''insert into `record`(`PID`,`TId`,`Amount`,salePrice) values(%s,%s,%s,%s)'''
        self.exec_cmd(sql,(pid,tid,amoumt,saleprice))


