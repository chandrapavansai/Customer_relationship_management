import sqlite3
import datetime


class service_staff():
    def __init__(self, id):
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        self.id = id
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

    def add_service_requests(self,user_id):
        con = sqlite3.connect('test.db')
        cur = con.cursor() 
        con.close()
        return [user_id,self.client_id,self.id]

    def get_myfeedback(self):
        con = sqlite3.connect('test.db')
        cur = con.cursor() 
        overall_feedback = []
        recent_feedback=[]
        overall_rating=0
        recent_rating=0
        overall_comments=[]
        recent_comments=[]
        query="""
            select user.name,ser_req.request,feedback.rating,feedback.comment,feedback.date_of_feedback
            from ser_req
            inner join user on feedback.user_id=user.id
            inner join feedback on ser_req.fd_id=feedback.fd_id
            where feedback.employee_id=?
        """
        result = [a for a in cur.execute(query,(self.id,))]
        print(result)
        for tpl in result:
            overall_feedback.append(tpl)
        # print(overall_feedback)
        temp1=sorted(overall_feedback,key=lambda x :x[4])
        # print(temp1)
        recent_feedback = temp1[-100:]
        # print(recent_feedback)
        # print(recent_feedback)
        # print(overall_feedback)
        temp=0
        count=0
        for j,i in enumerate(recent_feedback):
            temp+=recent_feedback[j][2]
            count+=1
            recent_comments.append(i)
        if count: recent_rating=temp/count
        else: recent_rating=0

        temp=0
        count=0
        for j,i in enumerate(overall_feedback):
            temp+=overall_feedback[j][2]
            count+=1
            overall_comments.append(i)
        # print(temp)
        if count: overall_rating=temp/count
        else: overall_rating=0
        con.close()
        return recent_comments,overall_comments,recent_rating,overall_rating
        

        


# temp = service_staff(13)
# print(temp.get_myfeedback())