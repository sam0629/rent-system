from dacs.dac import Dac


class SpaceTimeDac(Dac):
    def __init__(self):
        super().__init__()

    def qry_space_time(self, date, sid):
        sql = '''
            select st.SId, st.StartTime, st.TotalTime 
            from spaceTIME as st
            where 
                st.Date=%s and
                st.SId in %s
        '''

        return self.qry_all(sql, (date, sid))

    def qry_startandtotal_time(self, date, sid):
        sql = '''
        select  st.StartTime, st.TotalTime 
        from spaceTIME as st
        where 
	        st.Date=%s and
            st.SId = %s
    
        '''

        return self.qry_all(sql, (date, sid))

    def write(self,uid,sid,date,start_time,end_time,total_time,totalmoney):
        sql = '''insert into `spacetime`(`SID`,`UId`,`Date`,`StartTime`,`EndTime`,`TotalTime`,`TotalPrice`) values(%s,%s,%s,%s,%s,%s,%s)'''
        self.exec_cmd(sql,(uid,sid,date,start_time,end_time,total_time,totalmoney))
