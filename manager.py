import sqlite3
import datetime

class manager():
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
            WITH RECURSIVE rec AS (
                SELECT employee_id
                FROM man_emp
                WHERE manager_id = ? and manager_id <> employee_id

                UNION ALL

                SELECT m1.employee_id
                FROM man_emp as m1
                JOIN rec r ON m1.manager_id = r.employee_id
                where m1.manager_id <> m1.employee_id 
            )
            SELECT distinct(employee_id)
            FROM rec
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
        sales=[]
        query = """
            select id, name
            from employee
        """
        id_to_name_emp={}
        buf = [a for a in cur.execute(query)]
        for row in buf: id_to_name_emp[row[0]]=row[1]
        query = """
            select distinct(location)
            from user
        """
        locations = [a[0] for a in cur.execute(query)]
        for employee in self.employees:
            # print(employee)
            query = """
                select ifnull(sum(sales.sale_val),0) 
                from sales
                where sales.employee_id = ? 
                group by sales.employee_id
            """
            y = [a[0] for a in cur.execute(query,(employee,))]
            # print(y)
            x = 0
            if y : x=y[0]
            sales_employee[(id_to_name_emp[employee],employee)] = x
            total_sales += x
            # print(total_sales)
            query = """
                select sale_val, date, user.location
                from sales
                inner join user on user.id = sales.user_id
                where sales.employee_id = ?
            """
            x = [a for a in cur.execute(query,(employee,))]
            for row in x:
                sales.append(row)
                # print(row)
            for location in locations:
                query = """
                    select sum(sales.sale_val) 
                    from sales
                    inner join user on user.id = sales.user_id and user.location = ?
                    where sales.employee_id = ?
                    group by sales.employee_id
                """
                x = [a[0] for a in cur.execute(query,(location,employee,))]
                if not location in sales_area.keys(): sales_area[location]=0
                if x: sales_area[location] += x[0]
        ans=[]
        ans.append(total_sales)
        ans.append(sales_area)
        ans.append(sales_employee)
        ans.append(sales)
        con.close()
        return ans

    def feedback(self):
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        overall_feedback=0
        total_feedback=0
        total_count=0
        feedback_area={}
        feedback_employee={}
        feedback_area_count={}
        feedback_employee_count={}
        feedback=[]
        query = """
            select id, name
            from employee
        """
        id_to_name_emp={}
        buf = [a for a in cur.execute(query)]
        for row in buf: id_to_name_emp[row[0]]=row[1]
        query = """
            select distinct(location)
            from user
        """
        locations = [a[0] for a in cur.execute(query)]
        print(self.employees)
        for employee in self.employees:
            query = """
                select ifnull(sum(f.rating),0),count(*)
                from feedback as f
                where f.employee_id = ? 
                group by f.employee_id
            """
            y = [a for a in cur.execute(query,(employee,))]
            # print(y)
            x = 0; x1 = 1
            if y : 
                x=int(y[0][0]) 
                x1=int(y[0][1])
            feedback_employee[(id_to_name_emp[employee],employee)] = x
            feedback_employee_count[(id_to_name_emp[employee],employee)] = x1
            print(x)
            total_feedback += x
            total_count += x1
            query = """
                select rating, date_of_feedback, user.location
                from feedback
                inner join user on user.id = feedback.user_id
                where feedback.employee_id = ?
            """
            x = [a for a in cur.execute(query,(employee,))]
            for row in x:
                feedback.append(row)
            for location in locations:
                query = """
                    select ifnull(sum(f.rating),0),count(*)
                    from feedback as f
                    inner join user on user.id = f.user_id and user.location = ?
                    where f.employee_id = ? 
                    group by f.employee_id
                """
                x = [a for a in cur.execute(query,(location,employee,))]
                if not location in feedback_area.keys(): 
                    feedback_area[location]=0
                    feedback_area_count[location]=0
                if x: 
                    feedback_area[location] += int(x[0][0])
                    feedback_area_count[location] += int(x[0][1])
        ans=[]
        #print(total_feedback)
        ans.append(total_feedback/float(total_count))
        for location in locations:
            feedback_area[location]/=max(float(feedback_area_count[location]),1.0)
        ans.append(feedback_area)
        for employee in self.employees:
            feedback_employee[(id_to_name_emp[employee],employee)]/=max(float(feedback_employee_count[(id_to_name_emp[employee],employee)]),1.0)
        ans.append(feedback_employee)
        ans.append(feedback)
        con.close()
        return ans
        
    def performance(self):
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        total_rating=0
        no_of_ratings=0
        emp_avg_rating=[]
        tot_rating=0
        count=0
        for employee in self.employees:
            query = """
                select sum(rating),count(rating)
                from feedback
                where feedback.employee_id = ?
                group by feedback.employee_id
            """
            x = [a for a in cur.execute(query,(employee,))]
            for row in x:
                if row:
                    tot_rating+=int(row[0])
                    count+=int(row[1])
        con.close()
        if(count>0):
            return (tot_rating/count)
        else:
            return 0
    
    def hire(self,field_id,designation,name,password,email,ph_no):
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        query="""
            insert into employee(client_id,field_id,designation,name,pswrd,email,ph_no)
            values(?,?,?,?,?,?,?)
            
        """
        cur.execute(query,(self.client_id,field_id,designation,name,password,email,ph_no))
        con.commit()
        con.close()
        return 1

    def fire(self,id):
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        # print(id,1232132141)
        if not id in self.employees : return -1
        query="""
            delete from employee where id in ?
        """
        cur.execute(query,(id,))
        query="""
            delete from man_emp where employee_id = ? or manager_id = ?
        """
        cur.execute(query,(id,id))
        con.commit()
        
        con.close()
        return 1

# u = manager(5)
# u.fire(12)
# print(u.sales()[3])
# print(u.feedback()[0])

