from http.client import ImproperConnectionState
import sqlite3
from manager import *
from division_head import *
import datetime

class head():
    def __init__(self,id):
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
                select m.employee_id
                from man_emp as m
                inner join employee as e on e.designation = 'Division-Head' and e.id = m.employee_id
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
        total_sales=0
        sales_area={}
        sales_employee={}
        query = """
            select distinct(location)
            from user
        """
        locations = [a[0] for a in cur.execute(query)]
        total_sales = 0
        sales_yearly={}
        sales_monthly={}
        sales_field={}
        cur_time = str(datetime.date.today())
        cur_year = int(cur_time.split(' ')[0].split('-')[0])
        cur_month = int(cur_time.split(' ')[0].split('-')[1])
        sales_monthly_location={}
        sales_yearly_location={}
        sales_location={}
        for location in locations:
            sales_monthly_location[location]={}
            sales_yearly_location[location]={}
        for id in self.employees:
            x = division_head(id)
            buf_sales = x.sales()
            sales_field[x.field_id]=buf_sales[2]
            for key in buf_sales[0].keys():
                if not key in sales_yearly.keys(): sales_yearly[key]=0
                sales_yearly[key]+=buf_sales[0][key]
            for key in buf_sales[1].keys():
                if not key in sales_monthly.keys(): sales_monthly[key]=0
                sales_monthly[key]+=buf_sales[1][key]
            total_sales+=buf_sales[2]
            for key in buf_sales[3].keys():
                for inner_key in buf_sales[3][key].keys():
                    if not inner_key in sales_yearly_location[key].keys(): sales_yearly_location[key][inner_key]=0
                    sales_yearly_location[key][inner_key]+=buf_sales[3][key][inner_key]
            for key in buf_sales[4].keys():
                for inner_key in buf_sales[4][key].keys():
                    if not inner_key in sales_monthly_location[key].keys(): sales_monthly_location[key][inner_key]=0
                    sales_monthly_location[key][inner_key]+=buf_sales[4][key][inner_key]
            for key in buf_sales[5].keys():
                if not key in sales_location.keys(): sales_location[key]=0
                sales_location[key]+=buf_sales[5][key]
        
        con.close()
        ans=[]
        ans.append(sales_yearly)
        ans.append(sales_monthly)
        ans.append(total_sales)
        ans.append(sales_yearly_location)
        ans.append(sales_monthly_location)
        ans.append(sales_location)
        ans.append(sales_field)
        return ans


    def feedback(self):
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        total_feedback=0
        feedback_area={}
        feedback_employee={}
        query = """
            select distinct(location)
            from user
        """
        locations = [a[0] for a in cur.execute(query)]
        total_feedback = 0
        count=0
        feedback_yearly={}
        feedback_monthly={}
        feedback_yearly_count={}
        feedback_monthly_count={}
        feedback_field={}
        cur_time = str(datetime.date.today())
        cur_year = int(cur_time.split(' ')[0].split('-')[0])
        cur_month = int(cur_time.split(' ')[0].split('-')[1])
        feedback_monthly_location={}
        feedback_yearly_location={}
        feedback_monthly_location_count={}
        feedback_yearly_location_count={}
        feedback_location={}
        feedback_location_count={}
        for location in locations:
            feedback_monthly_location[location]={}
            feedback_yearly_location[location]={}
            feedback_monthly_location_count[location]={}
            feedback_yearly_location_count[location]={}
        for id in self.employees:
            x = division_head(id)
            buf_feedback = x.feedback()
            feedback_field[x.field_id]=buf_feedback[2]
            for key in buf_feedback[0].keys():
                if not key in feedback_yearly.keys(): 
                    feedback_yearly[key]=0
                    feedback_yearly_count[key]=0
                feedback_yearly[key]+=buf_feedback[0][key]*buf_feedback[6][key]
                feedback_yearly_count[key]+=buf_feedback[6][key]
            for key in buf_feedback[1].keys():
                if not key in feedback_monthly.keys(): 
                    feedback_monthly[key]=0
                    feedback_monthly_count[key]=0
                feedback_monthly[key]+=buf_feedback[1][key]*buf_feedback[7][key]
                feedback_monthly_count[key]+=buf_feedback[7][key]
            total_feedback+=buf_feedback[2]*buf_feedback[8]
            count+=buf_feedback[8]
            for key in buf_feedback[3].keys():
                for inner_key in buf_feedback[3][key].keys():
                    if not inner_key in feedback_yearly_location[key].keys(): 
                        feedback_yearly_location[key][inner_key]=0
                        feedback_yearly_location_count[key][inner_key]=0
                    feedback_yearly_location[key][inner_key]+=buf_feedback[3][key][inner_key]*buf_feedback[9][key][inner_key]
                    feedback_yearly_location_count[key][inner_key]+=buf_feedback[9][key][inner_key]
            for key in buf_feedback[4].keys():
                for inner_key in buf_feedback[4][key].keys():
                    if not inner_key in feedback_monthly_location[key].keys(): 
                        feedback_monthly_location[key][inner_key]=0
                        feedback_monthly_location_count[key][inner_key]=0
                    feedback_monthly_location[key][inner_key]+=buf_feedback[4][key][inner_key]*buf_feedback[10][key][inner_key]
                    feedback_monthly_location_count[key][inner_key]+=buf_feedback[10][key][inner_key]
            for key in buf_feedback[5].keys():
                if not key in feedback_location.keys(): 
                    feedback_location[key]=0
                    feedback_location_count[key]=0
                feedback_location[key]+=buf_feedback[5][key]*buf_feedback[11][key]
                feedback_location_count[key]+=buf_feedback[11][key]
        
        con.close()
        ans=[]
        for key in feedback_yearly.keys(): feedback_yearly[key]/=float(feedback_yearly_count[key])
        ans.append(feedback_yearly)
        for key in feedback_monthly.keys(): feedback_monthly[key]/=float(feedback_monthly_count[key])
        ans.append(feedback_monthly)
        total_feedback/=float(count)
        ans.append(total_feedback)
        for location in locations:
            for key in feedback_yearly_location[location].keys(): 
                feedback_yearly_location[location][key]/=float(feedback_yearly_location_count[location][key])
        ans.append(feedback_yearly_location)
        for location in locations:
            for key in feedback_monthly_location[location].keys(): 
                feedback_monthly_location[location][key]/=float(feedback_monthly_location_count[location][key])
        ans.append(feedback_monthly_location)
        for key in feedback_location.keys(): feedback_location[key]/=float(feedback_location_count[key])
        ans.append(feedback_location)
        ans.append(feedback_field)
        return ans


    def returning_customers(self):
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        # domains=[]
        query = """
            select domain.field_id
            from domain
            where client_id=?
        """
        y = [a[0] for a in cur.execute(query,(self.client_id,))]
        domain_ret_customers={}
        #print(self.client_id)

        for i in y: 
            query="""
                select u.id,u.name,u.email,u.profession,u.gender,u.location,count(*) as cnt
                from client as c
                inner join domain as d on d.client_id = c.id
                inner join field as f on f.id = d.field_id
                inner join employee as e on e.client_id = c.id and e.field_id = f.id
                inner join sales as s on s.employee_id = e.id
                inner join user as u on u.id = s.user_id
                where c.id = ? and f.id = ?
                group by u.id
                having cnt > 1
            """
            domain_ret_customers[i] = [a for a in cur.execute(query,(self.client_id,i,))]
        #print(domain_ret_customers)
        dict1={}
        for i in domain_ret_customers.keys():
            if domain_ret_customers[i]:
                dict1[i]=domain_ret_customers[i]
        con.close()
        return dict1

    def top_customers(self):
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        query="""
            select synergy.client_id,synergy.field_id,user.id,user.name,user.email,user.profession,user.gender,user.location,synergy.syn_val
            from user
            inner join synergy on user.id=synergy.user_id
            where synergy.client_id=? 
            order by synergy.syn_val desc
        """
        result= [a for a in cur.execute(query,(self.client_id,))]
        result=result[-10:]
        con.close()
        return result

    def suggestions(self):
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        a={}
        b={}
        c={}
        d={}
        query="""
            select field.id,field.name
            from field
        """
        result= [a for a in cur.execute(query)]
        # print(result)
        for i in result:
            d[i[0]]=i[1]
        # print(conv_id_name)
        for employee in self.employees:
            x = division_head(employee)
            buf =  x.sales()
            a[x.field_id] = buf[2]
            buf = x.feedback()
            b[x.field_id] = buf[2]
            c[x.field_id] = a[x.field_id]/float(b[x.field_id]+0.0001)
        ans=[]
        s = "The field with the lowest sales is "+d[(min(a, key=a.get))]
        ans.append(s)
        s = d[(min(b, key=b.get))]+" has the lowest customer satisfaction, therefore to maintain the user base in the sector must improve the customer relationship"
        ans.append(s)
        s = "The field with the lowest sales to feedback ratio is "+d[(min(c,key=c.get))]+" , therefore if a little restructuring is done to the sales counterpart of this field sales can increase in a significant amount"
        ans.append(s)
        con.close()
        return ans

k = head(1)
# print(k.employees)
# print(k.suggestions())
# print(k.returning_customers())