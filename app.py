# from load import *
from email import message
import datetime
from flask import Flask, render_template, redirect, url_for, request, session ,g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_session import Session
import json
from sqlalchemy import CheckConstraint
from manager import *
from division_head import *
from service_staff import *
from sales_rep import *
from head import *
import sqlite3

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route("/", methods = ['GET','POST'])
def login():
    session['id']=None
    error = None
    session.pop('id', None)
    if request.method == 'POST':
        id = request.form['id']
        id = int(id)
        pswrd = request.form['pswrd']
        l = db.engine.execute('select * from employee')
        f=0
        for i in l:
            if i['id']==id and i['pswrd']==pswrd:
                f=1
                session['id']=id
                if i['designation']=='manager':
                    return redirect(url_for('manager_login'))
                elif i['designation']=='Division-Head':
                    return redirect(url_for('divhead_login'))
                elif i['designation']=='service_staff':
                    return redirect(url_for('service_staff_login'))
                elif i['designation']=='Head':
                    return redirect(url_for('head_login'))                  
                else:
                    return redirect(url_for('sales_rep_login'))
        if f==0: error = 'Invalid credentials'
    return render_template("login.html", error = error)
    
@app.route("/manager")
def manager_login():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    sql = text('select * from employee as e where e.id = '+str(session.get('id')))
    l = db.engine.execute(sql)
    # u = manager_.manager(session.get('id'))
    # u.print_info()
    for i in l:
        if i['id']==int(session['id']):
            s=i['name']
            return render_template("manager.html",user_name=s)
        return "manager logged in"

@app.route("/divhead")
def divhead_login():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    sql = text('select * from employee as e where e.id = '+str(session.get('id')))
    l = db.engine.execute(sql)
    # u = manager_.manager(session.get('id'))
    # u.print_info()
    for i in l:
        if i['id']==int(session['id']):

            s=i['name']

            dh=division_head(int(session['id']))
            
            sales_yearly,sales_monthly,total_sales,sales_yearly_location,sales_monthly_location,sales_location=dh.sales()

            return render_template("divhead.html",user_name=s,sales_yearly=sales_yearly,sales_monthly=sales_monthly,total_sales=total_sales,sales_yearly_location=sales_yearly_location,sales_monthly_location=sales_monthly_location,sales_location=sales_location)
        return "divhead logged in"

@app.route("/service_staff")
def service_staff_login():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    sql = text('select * from employee as e where e.id = '+str(session.get('id')))
    l = db.engine.execute(sql)
    # u = manager_.manager(session.get('id'))
    # u.print_info()
    for i in l:
        if i['id']==int(session['id']):
            s=i['name']
            return render_template("service_staff.html",user_name=s)
        return "service_staff logged in"

@app.route("/sales_rep")
def sales_rep_login():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    sql = text('select * from employee as e where e.id = '+str(session.get('id')))
    l = db.engine.execute(sql)
    # u = manager_.manager(session.get('id'))
    # u.print_info()
    for i in l:
        if i['id']==int(session['id']):
            s=i['name']
            return render_template("sales_rep.html",user_name=s)
        return "sales representative logged in"


@app.route("/head")
def head_login():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    sql = text('select * from employee as e where e.id = '+str(session.get('id')))
    l = db.engine.execute(sql)
    # u = manager_.manager(session.get('id'))
    # u.print_info()
    for i in l:
        if i['id']==int(session['id']):
            s=i['name']
            return render_template("head.html",user_name=s)
        return "Head logged in"

@app.route("/manager/employees")
def manager_Employees():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    return render_template("Employees.html")

@app.route("/manager/my_performance")
def manager_MyPerformance():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    return render_template("my_performance.html")



# @app.route("/head")
# def head():
#         if not session.get('id'): return redirect("http://127.0.0.1:8000/")
#         sql = text('select * from employee as e where e.id = '+str(session.get('id')))
#         l = db.engine.execute(sql)
#         for i in l:
#             if i['id']==int(session['id']):
#                 s='Hi '+i['name']
#                 return s
#             return "manager logged in"


@app.route("/manager/employees/addemp", methods = ['GET','POST'])
def addemp():
     if not session.get('id'): return redirect("http://127.0.0.1:8000/")
     if request.method == 'POST':
        man_id=session.get('id')
        k=manager(man_id)
        k.hire(request.form['field'],request.form['designation'],request.form['name'],request.form['pswrd'],request.form['email'],request.form['phn'])
     return render_template("addemp.html")




@app.route("/manager/employees/removeemp", methods = ['GET','POST'])
def removeemp():
     if not session.get('id'): return redirect("http://127.0.0.1:8000/")
     if request.method == 'POST':
        man_id=session.get('id')
        k=manager(man_id)
        ret=k.fire(int(request.form['empid']))
        print(ret)
        if  ret== -1:
            print(11)
            error_rem='no such employee found'
            return render_template("removeemp.html",error_rem=error_rem)
     return render_template("removeemp.html")
    

@app.route("/sales_rep/addsale",methods=['GET','POST'])
def addsale_sales_rep():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    if request.method == 'POST':
        man_id=session.get('id')
        k=sales_rep(man_id)
        ans=k.addsale(int(request.form['user-id']),int(request.form['sales-val']))
        comment = str(request.form['field'])
        rating = 2.5
        # print(comment)
        # print(rating)
        if 'rate' in request.form:
            rating = int(request.form['rate'])
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        query = """
            insert into feedback(comment,rating,client_id,date_of_feedback,employee_id,user_id) values(?,?,?,?,?,?)
        """
        cur.execute(query,(comment,rating,ans[1],datetime.datetime.today(),ans[2],int(request.form['user-id'])))
        con.commit()
        query = """
            select max(fd_id)
            from feedback
        """
        feedback_id = [a[0] for a in cur.execute(query)][0]
        # print(feedback_id)
        query="""
                insert into sales(user_id,employee_id,fd_id,sale_val,date) values(?,?,?,?,?)
            """
        cur.execute(query,(int(request.form['user-id']),k.id,feedback_id,ans[0],datetime.datetime.today(),))
        con.commit()
        query="""
            select count(*)
            from synergy as s
            where user_id = ? and client_id = ? and field_id = ?
        """
        flag = [a for a in cur.execute(query,(int(request.form['user-id']),k.client_id,k.field_id,))]
        if flag and int(flag[0][0])>0:
            query="""
                    update synergy
                    set syn_val = 0.9*syn_val + 0.1*(?-2)*?
                    where user_id = ? and client_id = ? and field_id = ?
                """
            cur.execute(query,(rating,ans[0],int(request.form['user-id']),k.client_id,k.field_id,))
            con.commit()
        else : 
            query="""
                insert into synergy(user_id,client_id,field_id,syn_val) values(?,?,?,?)
            """
            new = 0.1*(rating-2)*ans[0]
            cur.execute(query,(int(request.form['user-id']),k.client_id,k.field_id,new,))
            con.commit()

        con.commit()
        con.close()
        if  not ans:
            # print(11)
            error_rem='Error Try again'
            return render_template("addsale.html",error_rem=error_rem)
    return render_template("addsale.html")
    

@app.route("/sales_rep/performance")
def sales_rep_performance():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    man_id=session.get('id')
    k=sales_rep(man_id)
    recent_comments,overall_comments,recent_rating,overall_rating=k.get_myfeedback()
    return render_template("performance.html",recent_comments=recent_comments,overall_comments=overall_comments,recent_rating=recent_rating,overall_rating=overall_rating)
   

@app.route("/sales_rep/profile")
def sales_rep_profile():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    k=sales_rep(session.get('id'))
    return render_template("profile.html",values=k.get_profile())

@app.route("/sales_rep/recent_sales")
def sales_rep_recent_sales():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    return render_template("recent_sales.html")


@app.route("/service_staff/profile")
def service_staff_profile():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    id=session.get('id')
    k=service_staff(id)
    return render_template("profile.html",values=k.get_profile())

@app.route("/service_staff/performance")
def service_staff_performance():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    man_id=session.get('id')
    k=service_staff(man_id)
    recent_comments,overall_comments,recent_rating,overall_rating=k.get_myfeedback()
    return render_template("service_request_performance.html",recent_comments=recent_comments,overall_comments=overall_comments,recent_rating=recent_rating,overall_rating=overall_rating)


@app.route("/service_staff/add_service_request",methods=['GET','POST'])
def service_staff_add_service_request():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    if request.method == 'POST':
        man_id=session.get('id')
        k=service_staff(man_id)
        ans=k.add_service_requests(int(request.form['user-id']))
        comment = str(request.form['feedback'])
        rating = 2.5
        # print(comment)
        # print(rating)
        if 'rate' in request.form:
            rating = int(request.form['rate'])
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        query = """
            insert into feedback(comment,rating,client_id,date_of_feedback,employee_id,user_id) values(?,?,?,?,?,?)
        """
        cur.execute(query,(comment,rating,ans[1],datetime.date.today(),ans[2],int(request.form['user-id'])))
        query = """
            select max(fd_id)
            from feedback
        """
        feedback_id = [a[0] for a in cur.execute(query)][0]
        print(feedback_id)
        query="""
                insert into ser_req(user_id,employee_id,fd_id,request,date) values(?,?,?,?,?)
            """
        cur.execute(query,(int(request.form['user-id']),ans[2],feedback_id,str(request.form['issue']),datetime.date.today(),))
        query="""
                update synergy
                set synergy.syn_val = 0.9*synergy.syn_val + 0.1*(?-2)*5
                where synergy.user_id = ? and synergy.client_id = ? and synergy.field_id = ?
            """
        cur.execute(query,(rating,int(request.form['user-id']),k.client_id,k.field_id,))
        con.commit()
        con.close()
        if  not ans:
            # print(11)
            error_rem='Error Try again'
            return render_template("add_service_request.html",error_rem=error_rem)
    return render_template("add_service_request.html")





@app.route("/manager/employees/confirm_add_emp", methods = ['GET','POST'])
def addempmanager():
    if request.method == 'POST':
        if not session.get('id'): return redirect("http://127.0.0.1:8000/")
        man_id=session.get('id')
        k=manager(man_id)
        k.hire(request.form['field_id'],request.form['designation'],request.form['name'],request.form['password'])


@app.route("/manager/profile")
def manager_profile():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    id=session.get('id')
    k=manager(id)
    return render_template("profile.html",values=k.get_profile())

@app.route("/manager/sales")
def manager_sales():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    man_id=session.get('id')
    k=manager(man_id)
    total_sales,sales_area,sales_employee,_=k.sales()
    return render_template("sales.html",sales_employee=sales_employee,sales_area=sales_area,total_sales=total_sales)

@app.route("/manager/rating")
def manager_rating():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    man_id=session.get('id')
    k=manager(man_id)
    total_rating,rating_area,rating_employee,_=k.feedback()
    return render_template("manager_rating.html",rating_employee=rating_employee,rating_area=rating_area,total_rating=total_rating)



@app.route("/division_head/profile")
def division_head_profile():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    id=session.get('id')
    k=division_head(id)
    return render_template("profile.html",values=k.get_profile())

@app.route("/division_head/sales")
def division_head_sales():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    id=session.get('id')
    k=division_head(id)
    
    sales_yearly,sales_monthly,total_sales,sales_yearly_location,sales_monthly_location,sales_location=k.sales()
    return render_template("division_head_sales.html",sales_yearly=sales_yearly,sales_monthly=sales_monthly,total_sales=total_sales,sales_yearly_location=sales_yearly_location,sales_monthly_location=sales_monthly_location,sales_location=sales_location)

@app.route("/division_head/feedback")
def division_head_feedback():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    id=session.get('id')
    k=division_head(id)
    sales_yearly,sales_monthly,total_sales,sales_yearly_location,sales_monthly_location,sales_location,_,_,_,_,_,_=k.feedback()
    return render_template("division_head_feedback.html",sales_yearly=sales_yearly,sales_monthly=sales_monthly,total_sales=total_sales,sales_yearly_location=sales_yearly_location,sales_monthly_location=sales_monthly_location,sales_location=sales_location)
        

@app.route("/division_head/potential_userbase")
def division_head_potential_userbase():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    id=session.get('id')
    k=division_head(id)
    value=k.potential_user_base()
    return render_template("division_head_potential_userbase.html", values=value)



@app.route("/head/profile")
def head_profile():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    id=session.get('id')
    k=head(id)
    return render_template("profile.html",values=k.get_profile())

@app.route("/head/sales")
def head_sales():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    id=session.get('id')
    k=head(id)
    sales_yearly,sales_monthly,total_sales,sales_yearly_location,sales_monthly_location,sales_location,sales_field=k.sales()
    return render_template("head_sales.html",sales_yearly=sales_yearly,sales_monthly=sales_monthly,total_sales=total_sales,sales_yearly_location=sales_yearly_location,sales_monthly_location=sales_monthly_location,sales_location=sales_location,sales_field=sales_field)

@app.route("/head/feedback")
def head_feedback():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    id=session.get('id')
    k=head(id)
    feedback_yearly,feedback_monthly,total_feedback,feedback_yearly_location,feedback_monthly_location,feedback_location,feedback_field=k.feedback()
    return render_template('head_feedback.html',feedback_yearly=feedback_yearly,feedback_monthly=feedback_monthly,total_feedback=total_feedback,feedback_yearly_location=feedback_yearly_location,feedback_monthly_location=feedback_monthly_location,feedback_location=feedback_location,feedback_field=feedback_field)

@app.route("/head/sectorwiseanalysis")
def head_secwise_analysis():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    id=session.get('id')
    k=head(id)
    sales_yearly,sales_monthly,total_sales,sales_yearly_location,sales_monthly_location,sales_location,sales_field=k.sales()
    feedback_yearly,feedback_monthly,total_feedback,feedback_yearly_location,feedback_monthly_location,feedback_location,feedback_field=k.feedback()
    return render_template('head_sectorwiseanalysis.html',sales_yearly=sales_yearly,sales_monthly=sales_monthly,total_sales=total_sales,sales_yearly_location=sales_yearly_location,sales_monthly_location=sales_monthly_location,sales_location=sales_location,sales_field=sales_field,feedback_yearly=feedback_yearly,feedback_monthly=feedback_monthly,total_feedback=total_feedback,feedback_yearly_location=feedback_yearly_location,feedback_monthly_location=feedback_monthly_location,feedback_location=feedback_location,feedback_field=feedback_field)

# @app.route("/head/returning_customers")
# def ret_customers():
#     if not session.get('id'): return redirect("http://127.0.0.1:8000/")
#     id=session.get('id')
#     k=head(id)
#     domain_wise_ret_customers = k.returning_customers()
#     return render_template('head_ret_customers.html',domain_wise_ret_customers=domain_wise_ret_customers)

# @app.route("/head/top_customers")
# def top_customers():
#     if not session.get('id'): return redirect("http://127.0.0.1:8000/")
#     id=session.get('id')
#     k=head(id)
#     return render_template('head_top_customers.html',top_customers=top_customers)

@app.route("/head/suggestions")
def suggestions():
    if not session.get('id'): return redirect("http://127.0.0.1:8000/")
    id=session.get('id')
    k=head(id)
    domain_wise_ret_customers = k.returning_customers()
    top_customers = k.top_customers()
    suggestions=k.suggestions()
    return render_template('head_suggestions.html',top_customers=top_customers,domain_wise_ret_customers=domain_wise_ret_customers,suggestions=suggestions)

db.session.commit()

if __name__=="__main__":
    app.run(debug=True, port=8000)





