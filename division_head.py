from http.client import ImproperConnectionState
import sqlite3
from manager import *
import datetime

class division_head():
    def __init__(self, id):
        self.id = id
        con = sqlite3.connect('test.db')
        cur = con.cursor() 
        query = """
            select client_id
            from employee
            where employee.id = ?
        """
        self.client_id = [a[0] for a in cur.execute(query,(id,))][0]
        query = """
            select field_id
            from employee
            where employee.id = ?
        """
        self.field_id = [a[0] for a in cur.execute(query,(id,))][0]
        query = """
            select m.employee_id
            from man_emp as m
            where m.manager_id = ?
        """
        self.employees = [a[0] for a in cur.execute(query,(id,))]
        con.close()

    def get_profile(self):
        con = sqlite3.connect('test.db')
        cur = con.cursor() 
        query="""
            select employee.id,employee.name,employee.designation,field.name,client.name,employee.email,employee.ph_no
            from employee
            inner join client on client.id=employee.client_id
            inner join field on field.id=employee.field_id
            where employee.id=?
        """
        result = [a for a in cur.execute(query,(self.id,))]
        con.close()

        return result

    def print_info(self):
        con = sqlite3.connect('test.db')
        cur = con.cursor() 
        table_list = [a for a in cur.execute("SELECT * FROM employee where id=?",(self.id,))]
        print(table_list)
        con.close()
    
    def sales(self):
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        total_sales = 0
        sales_yearly={}
        sales_monthly={}
        cur_time = str(datetime.date.today())
        cur_year = int(cur_time.split(' ')[0].split('-')[0])
        cur_month = int(cur_time.split(' ')[0].split('-')[1])
        locations = [a[0] for a in cur.execute("SELECT distinct(location) FROM user")]
        # print(locations)
        sales_monthly_location={}
        sales_yearly_location={}
        sales_location={}
        for location in locations:
            sales_monthly_location[location]={}
            sales_yearly_location[location]={}
        for id in self.employees:
            x = manager(id)
            buf_sales = x.sales()[3]
            # print(buf_sales)
            # print(buf_sales)
            for row in buf_sales:
                total_sales+=int(row[0])
                #print(row)
                year = int(row[1].split(' ')[0].split('-')[0])
                month = int(row[1].split(' ')[0].split('-')[1])
                location = row[2]
                if not location in sales_location.keys(): sales_location[location]=0
                sales_location[location]+=int(row[0])
                if not year in sales_yearly.keys() : sales_yearly[year]=0 
                if not year in sales_yearly_location[location].keys() : sales_yearly_location[location][year]=0 
                sales_yearly[year]+=int(row[0])
                sales_yearly_location[location][year]+=int(row[0])
                x = 12*(cur_year-year)+cur_month-month
                if x>12 : continue
                if not 12-x in sales_monthly.keys(): sales_monthly[12-x]=0
                if not 12-x in sales_monthly_location[location].keys(): sales_monthly_location[location][12-x]=0
                sales_monthly[12-x]+=int(row[0])
                sales_monthly_location[location][12-x]+=int(row[0])
        con.close()
        ans=[]
        ans.append(sales_yearly)
        ans.append(sales_monthly)
        ans.append(total_sales)
        ans.append(sales_yearly_location)
        ans.append(sales_monthly_location)
        ans.append(sales_location)
        return ans

    def feedback(self):
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        feedback_yearly={}
        feedback_yearly_count={}
        feedback_monthly={}
        feedback_monthly_count={}
        cur_time = str(datetime.date.today())
        cur_year = int(cur_time.split(' ')[0].split('-')[0])
        cur_month = int(cur_time.split(' ')[0].split('-')[1])
        locations = [a[0] for a in cur.execute("SELECT distinct(location) FROM user")]
        feedback_monthly_location={}
        feedback_monthly_location_count={}
        feedback_yearly_location={}
        feedback_yearly_location_count={}
        feedback_location={}
        feedback_location_count={}
        for location in locations:
            feedback_monthly_location[location]={}
            feedback_yearly_location[location]={}
            feedback_monthly_location_count[location]={}
            feedback_yearly_location_count[location]={}
        total_feedback = 0
        count = 0
        for id in self.employees:
            x = manager(id)
            buf_feedback = x.feedback()[3]
            for row in buf_feedback:
                total_feedback+=int(row[0])
                count+=1
                year = int(row[1].split(' ')[0].split('-')[0])
                month = int(row[1].split(' ')[0].split('-')[1])
                location = row[2]
                if not location in feedback_location.keys(): 
                    feedback_location[location]=0
                    feedback_location_count[location]=0
                if not year in feedback_yearly_location[location].keys() : 
                    feedback_yearly_location[location][year]=0
                    feedback_yearly_location_count[location][year]=0
                feedback_yearly_location[location][year]+=int(row[0])
                feedback_yearly_location_count[location][year]+=1
                feedback_location[location]+=int(row[0])
                feedback_location_count[location]+=1
                if not year in feedback_yearly.keys() : 
                    feedback_yearly[year]=0 
                    feedback_yearly_count[year]=0 
                feedback_yearly[year]+=int(row[0])
                feedback_yearly_count[year]+=1
                x = 12*(cur_year-year)+cur_month-month
                if x>12 : continue
                if not 12-x in feedback_monthly.keys(): 
                    feedback_monthly[12-x]=0
                    feedback_monthly_count[12-x]=0
                if not 12-x in feedback_monthly_location[location].keys() : 
                    feedback_monthly_location[location][12-x]=0
                    feedback_monthly_location_count[location][12-x]=0
                feedback_monthly_location[location][12-x]+=int(row[0])
                feedback_monthly_location_count[location][12-x]+=1
                feedback_monthly[12-x]+=int(row[0])
                feedback_monthly_count[12-x]+=1
        con.close()
        ans=[]
        for key in feedback_yearly.keys(): feedback_yearly[key]/=max(float(feedback_yearly_count[key]),1.0)
        ans.append(feedback_yearly)
        for key in feedback_monthly.keys(): feedback_monthly[key]/=max(float(feedback_monthly_count[key]),1.0)
        ans.append(feedback_monthly)
        ans.append(total_feedback/max(float(count),1.0))
        for location in locations:
            for key in feedback_yearly_location[location].keys(): 
                feedback_yearly_location[location][key]/=max(float(feedback_yearly_location_count[location][key]),1.0)
        ans.append(feedback_yearly_location)
        for location in locations:
            for key in feedback_monthly_location[location].keys(): 
                feedback_monthly_location[location][key]/=max(float(feedback_monthly_location_count[location][key]),1.0)
        ans.append(feedback_monthly_location)
        for key in feedback_location.keys(): feedback_location[key]/=max(float(feedback_location_count[key]),1.0)
        ans.append(feedback_location)
        ans.append(feedback_yearly_count)
        ans.append(feedback_monthly_count)
        ans.append(count)
        ans.append(feedback_yearly_location_count)
        ans.append(feedback_monthly_location_count)
        ans.append(feedback_location_count)
        return ans

    def potential_user_base(self):
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        query="""
            select distinct(u.id), u.name, u.email, u.profession, u.gender, u.location
            from user as u
            inner join synergy as s on s.user_id = u.id
            inner join client as c on c.id <> ?
            where s.field_id = ? and s.syn_val>35 and u.id not in 
            (select u1.id 
            from user as u1 
            inner join synergy as s1 on s1.user_id=u1.id 
            where s1.client_id=?)
        """
        x = [a for a in cur.execute(query,(self.client_id,self.field_id,self.client_id))]
        return x
        
 # inner join client as c on c.id <> s.client_id
            # inner join domain as d on d.client_id = c.id
            #

# u = division_head(2)
# print(u.potential_user_base())
# print(ans[0])
# print(ans[1])
# print(ans[2])
# print(ans[3])
# print(ans[4])
# print(ans[5])







