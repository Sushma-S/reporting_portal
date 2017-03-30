
from flask_wtf import *
from wtforms import *
from flask import *
from flask_admin.form import DatePickerWidget
from flaskext.mysql import MySQL
import csv
import xlsxwriter
from xlsxwriter.workbook import Workbook
import os
import datetime
import flask
 
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'project'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL(app)
    
@app.route('/home')
    
def home():
    return render_template('login.html')
                
    
@app.route('/login', methods = ['GET','POST'])
    
def login_name():
    username = request.form['username']
    password = request.form['password']

    cursor = mysql.get_db().cursor()

    cursor.execute("select * from login where name='" + username + "' and password='" + password + "'")

    data = cursor.fetchall()
    if data:
        session['logged_in'] = True
        #return "<label>&emsp;Hi " +username+ "</label>" +home1()
        return app_option("Hi "+username+",")

    else:
        error="Invalid Username or Password!!!"
        return render_template("login.html",error = error)

    return home()

def app_option(user):
	return render_template('option.html',user=user)

@app.route("/app_option",methods=['GET','POST'])
def app_option_validate():
    if request.method == 'POST':
        option = request.form['options']
        if option=="":
            return app_option("hi")
        elif option=="Azure":
        	return "hello"
        else:
        	return date_input("Hi")

def date_input(user):
	return render_template('date_input1.html',user=user)


@app.route("/date", methods = ['GET', 'POST'])

def date_inputs():
	if request.method == 'POST':
		start_date1 = request.form['start_date']
		end_date1 = request.form['end_date']
		if start_date1 != "" and end_date1 != "":
			f = '%d/%m/%Y'
           		start_date = datetime.datetime.strptime(start_date1, f)
           		end_date = datetime.datetime.strptime(end_date1, f)
           		if start_date != "" and end_date != "" and start_date < end_date:
            			error=""                        			
            			return checkbox_options(start_date,end_date,error)
           		else:
                		error="Enter valid start date and end date"
                		return render_template("date_input1.html",error = error)
		else:
			error="Enter valid start date and end date"
			return render_template("date_input1.html",error = error)


def checkbox_options(start_date,end_date,error):
    return render_template('checkbox_options.html',date = start_date, date1 = end_date,error=error)


@app.route("/no_parameters", methods = ['GET','POST'])

def no_parameters():
        start_date=request.form['date']
        end_date=request.form['date1']

        cursor = mysql.get_db().cursor()
    	start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    	end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
        #row_count=cursor.execute("select 'wallet_id','name','product','startdate','enddate' union all select * from wallet_info where startdate >= '" + start_date + "'and enddate <= '" + end_date + "'")
    	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where SaleDate >= '" + str(start_date) + "'and SaleDate <= '" + str(end_date) + "' limit 20")

        if row_count > 1:

                row = cursor.fetchall()
                workbook =xlsxwriter.Workbook('output.xlsx')
                sheet = workbook.add_worksheet()
                for r, row1 in enumerate(row):
                        for c, col in enumerate(row1):
                                sheet.write(r, c, col)

               # return '<html> <body> Data copied to XLSX file <a href = "/downloadCSV"> Click here to download. </a>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; <a href="/logout"><b>Logout</b></a></body> </html>'
        	return render_template("download.html")

        else:
        	error="No transaction found!!!"
                return checkbox_options(start_date,end_date,error)



@app.route("/parameter", methods = ['GET','POST'])

def parameters():
	if request.method == 'POST':
		wallet_id=request.form['wallet_id']
        	transid = request.form['Transid']
    		product=request.form['product']
    		saledatekey=request.form['saledatekey']
		mdn=request.form['mdn']
		start_date=request.form['date']
        	end_date=request.form['date1']	
        	cursor = mysql.get_db().cursor()
    		
		if request.form.get("wallet_op") and request.form.get("product_op") and request.form.get("Transid_op") and request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and ProductName='" + product + "'and TransID = '" +transid+ "'and SaleDateKey = '" +saledatekey+ "'and MDN = '" +mdn+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")

		elif request.form.get("wallet_op") and request.form.get("product_op") and request.form.get("Transid_op") and request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and ProductName='" + product + "'and TransID = '" +transid+ "'and SaleDateKey = '" +saledatekey+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif request.form.get("wallet_op") and request.form.get("product_op") and request.form.get("Transid_op") and not request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and ProductName='" + product + "'and TransID = '" +transid+ "'and MDN = '" +mdn+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif request.form.get("wallet_op") and request.form.get("product_op") and not request.form.get("Transid_op") and request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and ProductName='" + product + "'and MDN = '" +mdn+ "'and MDN = '" +mdn+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif request.form.get("wallet_op") and not request.form.get("product_op") and request.form.get("Transid_op") and request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and MDN='" + mdn + "'and TransID = '" +transid+ "'and MDN = '" +mdn+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif not request.form.get("wallet_op") and request.form.get("product_op") and request.form.get("Transid_op") and request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where MDN='" + mdn + "'and ProductName='" + product + "'and TransID = '" +transid+ "'and MDN = '" +mdn+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")


		elif request.form.get("wallet_op") and request.form.get("product_op") and request.form.get("Transid_op") and not request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and ProductName='" + product + "'and TransID = '" +transid+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif request.form.get("wallet_op") and request.form.get("product_op") and not request.form.get("Transid_op") and request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and ProductName='" + product + "'and SaleDateKey = '" +saledatekey+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif request.form.get("wallet_op") and not request.form.get("product_op") and request.form.get("Transid_op") and request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and TransID = '" +transid+ "'and SaleDateKey = '" +saledatekey+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif not request.form.get("wallet_op") and request.form.get("product_op") and request.form.get("Transid_op") and request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select * from FactMasterB2B USE INDEX (report_idx) where ProductName='" + product + "'and TransID = '" +transid+ "'and SaleDateKey = '" +saledatekey+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif not request.form.get("wallet_op") and not request.form.get("product_op") and request.form.get("Transid_op") and request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where MDN='" + mdn + "'and TransID = '" +transid+ "'and SaleDateKey = '" +saledatekey+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif not request.form.get("wallet_op") and request.form.get("product_op") and not request.form.get("Transid_op") and request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where ProductName='" + product + "'and MDN = '" +mdn+ "'and SaleDateKey = '" +saledatekey+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif not request.form.get("wallet_op") and request.form.get("product_op") and request.form.get("Transid_op") and not request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where ProductName='" + product + "'and TransID = '" +transid+ "'and MDN = '" +mdn+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif request.form.get("wallet_op") and not request.form.get("product_op") and not request.form.get("Transid_op") and request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and SaleDateKey = '" +saledatekey+ "'and MDN = '" +mdn+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif request.form.get("wallet_op") and not request.form.get("product_op") and request.form.get("Transid_op") and not request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and TransID = '" + transid + "'and MDN = '" + mdn + "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif request.form.get("wallet_op") and request.form.get("product_op") and not request.form.get("Transid_op") and not request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and ProductName = '" + product + "'and MDN = '" + mdn + "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")

		elif request.form.get("wallet_op") and request.form.get("product_op") and not request.form.get("Transid_op") and not request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and ProductName='" + product + "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif not request.form.get("wallet_op") and not request.form.get("product_op") and request.form.get("Transid_op") and request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where TransID = '" +transid+ "'and SaleDateKey = '" +saledatekey+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif not request.form.get("wallet_op") and request.form.get("product_op") and not request.form.get("Transid_op") and request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where ProductName='" + product + "'and SaleDateKey = '" +saledatekey+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif not request.form.get("wallet_op") and request.form.get("product_op") and request.form.get("Transid_op") and not request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where ProductName='" + product + "'and TransID = '" +transid+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif request.form.get("wallet_op") and not request.form.get("product_op") and not request.form.get("Transid_op") and request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and SaleDateKey = '" +saledatekey+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif request.form.get("wallet_op") and not request.form.get("product_op") and request.form.get("Transid_op") and not request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and TransID = '" +transid+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif request.form.get("wallet_op") and not request.form.get("product_op") and not request.form.get("Transid_op") and not request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and MDN = '" + mdn + "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif not request.form.get("wallet_op") and request.form.get("product_op") and not request.form.get("Transid_op") and not request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where ProductName='" + product + "'and MDN = '" + mdn + "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif not request.form.get("wallet_op") and not request.form.get("product_op") and request.form.get("Transid_op") and not request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where TransID='" + transid + "'and MDN = '" + mdn + "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif not request.form.get("wallet_op") and not request.form.get("product_op") and not request.form.get("Transid_op") and request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where SaleDateKey='" + saledatekey + "'and MDN = '" + mdn + "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")

		elif not request.form.get("wallet_op") and not request.form.get("product_op") and not request.form.get("Transid_op") and not request.form.get("saledatekey_op") and request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where MDN = '" + mdn + "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif not request.form.get("wallet_op") and not request.form.get("product_op") and not request.form.get("Transid_op") and request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where SaleDateKey = '" +saledatekey+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif request.form.get("wallet_op") and not request.form.get("product_op") and not request.form.get("Transid_op") and not request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where WalletID='" + wallet_id + "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif not request.form.get("wallet_op") and request.form.get("product_op") and not request.form.get("Transid_op") and not request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where ProductName='" + product + "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")
		elif not request.form.get("wallet_op") and not request.form.get("product_op") and request.form.get("Transid_op") and not request.form.get("saledatekey_op") and not request.form.get("mdn_op"):
                	row_count=cursor.execute("select 'FactID','TransactionNumber','TransactionTypeID','SaleDateKey','SaleDate','WalletID','WalletKey','MDN','BelongsTo','WalletTypeID','WalletOwnerID','MerchantTypeID','BusinessCityID','BusinessDistrictID','BusinessStateID','ProductID','ProductName','ProcessorID','GenericProcessorID','PackageID','ProductCategoryID','OperatorID','FaceValue','SalesValue','Surcharge','TerminalID','TerminalTypeID','TransactionRef','Description','Request','Agent','InstrumentID','IsAutoReversal','NetSalesValue','vwallet','BelongsToKey','originalTransactionNumber','Originaltransdate','MobileNumber','CurrentBalance','OriginalTransactionAmount','PartnerRequestID_AGG','OperatorTransactionID','ReplyMessage_AGG','IsBilled','ResParam1','ResParam2','ResParam3','ResParam4','TransID','BankRefNo','ReplyMessage_INT','PartnerRequestID_SD','Q7_FD','Q9_FD' union all select * from FactMasterB2B USE INDEX (report_idx) where TransID = '" +transid+ "'and SaleDate >= '" + start_date + "'and SaleDate <= '" + end_date + "' limit 20")




		else:
        		error="Please input information!!!!!"
        		return checkbox_options(start_date,end_date,error)
    
        
		if row_count > 1:
			row = cursor.fetchall()
            		workbook =xlsxwriter.Workbook('output.xlsx')
            		sheet = workbook.add_worksheet()
                	for r, row1 in enumerate(row):
                    		for c, col in enumerate(row1):
                            		sheet.write(r, c, col)

                #return '<html> <body> Data copied to XLSX file <a href = "/downloadCSV"> Click here to download. </a>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; <a href="/logout"><b>Logout</b></a></body> </html>'
                	return render_template("download.html")

        	else:
        		error="No transaction found!!!"
        		return checkbox_options(start_date,end_date,error)

@app.route("/downloadXLSX")

def downloadExcel():
	excelDownload = open("output.xlsx",'rb').read()
	return Response(
        	excelDownload,
        	mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        	headers={"Content-disposition":
                 "attachment; filename=output.xlsx"})


@app.errorhandler(404)
def pagenotfound(e):
	return render_template("404.html")

@app.route("/logout")

def logout():
    session['logged_in'] = False   
    return redirect(url_for('home'))
    #return home()


if __name__ == "__main__":
        app.secret_key = os.urandom(12)
        app.run(debug = True)


