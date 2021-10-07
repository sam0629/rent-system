from dacs.dac import Dac


class ProductDac(Dac):
    def __init__(self):
        super().__init__()

    def qry_pType(self):
        sql = '''
        select  PType 
        from product group by PType'''
        return self.qry_all(sql)

    def read_product_by_type(self,type):
        sql = '''
        select  *
        from product
        where PType = %s'''
        return self.qry_all(sql,type)

    def read_all_product(self):
        sql = '''
        select  *
        from product'''
        return self.qry_all(sql)

    def is_true_product(self,pid,pname):
        sql ='''
        select PId
        from product
        where PId = %s and PName = %s
        '''
        return self.qry_one(sql,(pid,pname)) is not None

    def is_correct_product_and_get_amount(self,pid,pname,pamount):
        sql ='''
        select PNumber
        from product 
        where PId = %s and PName = %s
        '''
        return self.qry_one(sql,(pid,pname))
    def qry_unit_price(self,pid):
        sql = '''
               select PUnitPrice
               from product 
               where PId = %s
               '''
        return self.qry_one(sql,pid)
