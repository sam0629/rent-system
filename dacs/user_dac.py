from dacs.dac import Dac


class UserDac(Dac):
    def __init__(self):
        super().__init__()

    # 抓出資料庫uName存入username回傳,輸入的帳密不存在資料庫回傳None
    def read_uid(self, account, password):
        sql = "SELECT `UId` FROM `user` where `UAccount` = %s and `UPassword` = %s"
        return self.qry_one(sql, (account, password))

    def read_uname(self, uid):
        sql = "SELECT `UName` FROM `user` where `UId` = %s"
        return self.qry_one(sql, (uid))

    def read_uaccount(self, uaccount):
        sql = "SELECT * FROM `user` where `UAccount` = %s"
        return self.qry_one(sql, uaccount)

    def add_user(self, uname, uaccount, upassword):
        sql = "INSERT INTO `User` (`UName`, `UAccount`,`UPassword`) VALUES (%s, %s,%s)"
        self.exec_cmd(sql, (uname, uaccount, upassword))
