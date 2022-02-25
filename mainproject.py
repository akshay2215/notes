from flask import Flask,render_template,request
import pymysql

db=None
cur=None

def connectDb():
    global db,cur
    db=pymysql.connect(host="localhost",
                        user="root",
                        password="",
                        database="bank")
    cur=db.cursor()

def disconnectDb():
    cur.close()
    db.close()


def readRecords():
    connectDb()
    selectquery="select * from bankdata"
    cur.execute(selectquery)
    result=cur.fetchall()
    disconnectDb()
    return result 

def insertTobankTable(FName,LName,Email,AccNo,IFSCCode,Balance):
    connectDb()
    insertquery="insert into bankdata(FName,LName,Email,AccNo,IFSCCode,Balance) values('{}','{}','{}','{}','{}','{}')".\
        format(FName,LName,Email,AccNo,IFSCCode,Balance)
    cur.execute(insertquery)
    db.commit()
    disconnectDb()

def deleteFrombankTable(FName):
    connectDb()
    deletequery="delete from bankdata where FName='{}'".format(FName)
    cur.execute(deletequery)
    db.commit()
    disconnectDb()

def getoneempRecord(FName):
    connectDb()
    selectquery="select * from bankdata where FName='{}'".format(FName)
    cur.execute(selectquery)
    result=cur.fetchone()
    disconnectDb()
    return result 

def updatebankTable(FName,LName,Email,AccNo,IFSCCode,Balance):
    connectDb()
    updatequery='update bankdata set FName="{}", \
                LName="{}", Email="{}",AccNo="{}",IFSCCode="{}",Balance="{}" where FName="{}"'.\
                    format(FName,LName,Email,AccNo,IFSCCode,Balance,FName)
    cur.execute(updatequery)
    db.commit()
    disconnectDb()



app=Flask(__name__)

@app.route('/')
def home():
    data=readRecords()
    return render_template('index.html',data=data)

@app.route('/user',methods=['GET','POST'])
def show():
      data=readRecords()
      return render_template('display.html',message='All Employees',data=data)
      
      
@app.route('/adduser',methods=['GET','POST'])
def addemp():
    if request.method=='POST':
        insertTobankTable(request.form['Fname'],
            request.form['LName'],request.form['Email'],request.form['AccNo'],request.form['IFSCCode'],request.form['Balance'])
        data=readRecords()
        return render_template('index.html',message='Employee Inserted successfully',data=data)
    else:
        return render_template('add.html')

@app.route('/delete/<id>')
def deletebank(id):
    deleteFrombankTable(id)
    data=readRecords()
    return render_template('display.html',message="Delete Completed",data=data)

@app.route('/update/<FName>',methods=['GET','POST'])
def updateEmp(FName): 
    if request.method=='POST':
        updatebankTable(FName,request.form['LName'],request.form['Email'],request.form['AccNo'],request.form['IFSCCode'],request.form['Balance'])
        data=readRecords()
        return render_template('display.html',message='Update Completed',data=data)
    else:
        data=getoneempRecord(FName)
        return render_template('update.html',data=data)


if __name__=='__main__':
    app.run(debug=True)