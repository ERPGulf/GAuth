import requests
import json
import frappe
import json
import urllib.parse;
import base64
from frappe.utils.image import optimize_image
import os
from frappe.utils import cint
from mimetypes import guess_type
from typing import TYPE_CHECKING
from werkzeug.wrappers import Response
from frappe.utils.password import update_password as _update_password
from frappe.core.doctype.user.user import update_password as _update_password_reset_key
from frappe.utils import now
import random
from frappe.core.doctype.user.user import User
from frappe.utils import get_url
from frappe import _, is_whitelisted, ping
from frappe.utils import (
	now_datetime
)
from frappe.utils import add_days, flt

from erpnext.accounts.report.financial_statements import get_data, get_period_list
from erpnext.accounts.utils import get_balance_on, get_fiscal_year


error='Authentication required. Please provide valid credentials..'

@frappe.whitelist(allow_guest=True)
def getToken2(self):
    pass


@frappe.whitelist(allow_guest=True)
def test_api():
    return "test api success"


@frappe.whitelist(allow_guest=True)
def generate_token_secure( api_key, api_secret, app_key):
    # frappe.log_error(title='Login attempt',message=str(api_key) + str(api_secret) + str(app_key + "  "))
    try:
        try:
            app_key = base64.b64decode(app_key).decode("utf-8")
        except Exception as e:
            return Response(json.dumps({"message": "Security Parameters are not valid" , "user_count": 0}), status=401, mimetype='application/json')
        clientID, clientSecret, clientUser = frappe.db.get_value('OAuth Client', {'app_name': app_key}, ['client_id', 'client_secret','user'])
        
        if clientID is None:
            # return app_key
            return Response(json.dumps({"message": "Security Parameters are not valid" , "user_count": 0}), status=401, mimetype='application/json')
        
        client_id = clientID  # Replace with your OAuth client ID
        client_secret = clientSecret  # Replace with your OAuth client secret
        url =  frappe.local.conf.host_name  + "/api/method/frappe.integrations.oauth2.get_token"
        payload = {
            "username": api_key,
            "password": api_secret,
            "grant_type": "password",
            "client_id": client_id,
            "client_secret": client_secret,
            # "grant_type": "refresh_token"
        }
        files = []
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, files=files)
        if response.status_code == 200:
            result_data = json.loads(response.text)
            return Response(json.dumps({"data":result_data}), status=200, mimetype='application/json')
            
        else:
            frappe.local.response.http_status_code = 401
            return json.loads(response.text)
            
    except Exception as e:
            # frappe.local.response.http_status_code = 401
            # return json.loads(response.text)
            return Response(json.dumps({"message": e , "user_count": 0}), status=500, mimetype='application/json')
        
        
        
@frappe.whitelist(allow_guest=False)
def generate_token_secure_for_users( username, password, app_key):
    
    # return Response(json.dumps({"message": "2222 Security Parameters are not valid" , "user_count": 0}), status=401, mimetype='application/json')
    frappe.log_error(title='Login attempt',message=str(username) + "    " + str(password) + "    " + str(app_key + "  "))
    try:
        try:
            app_key = base64.b64decode(app_key).decode("utf-8")
        except Exception as e:
            return Response(json.dumps({"message": "Security Parameters are not valid" , "user_count": 0}), status=401, mimetype='application/json')
        clientID, clientSecret, clientUser = frappe.db.get_value('OAuth Client', {'app_name': app_key}, ['client_id', 'client_secret','user'])
        
        if clientID is None:
            # return app_key
            return Response(json.dumps({"message": "Security Parameters are not valid" , "user_count": 0}), status=401, mimetype='application/json')
        
        client_id = clientID  # Replace with your OAuth client ID
        client_secret = clientSecret  # Replace with your OAuth client secret
        url =  frappe.local.conf.host_name  + "/api/method/frappe.integrations.oauth2.get_token"
        payload = {
            "username": username,
            "password": password,
            "grant_type": "password",
            "client_id": client_id,
            "client_secret": client_secret,
            # "grant_type": "refresh_token"
        }
        files = []
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, files=files)
        # var = frappe.get_list("Customer", fields=["name as id", "full_name","email", "mobile_no as phone",], filters={'name': ['like', username]})
        qid=frappe.get_list("Customer", fields=["name as id","custom_full_name as  full_name","custom_mobile_number as phone","name as email","custom_qid as qid"], filters={'name': ['like', username]})
        if response.status_code == 200:
            doc=frappe.get_doc({
            "doctype": "log_in details",
            "user":username,
            "time":now_datetime(),
           }).insert(ignore_permissions=True)
            response_data = json.loads(response.text)
            
            result = {
                "token": response_data,
                "user": qid[0] if qid else {} ,
                "time":str(now_datetime())
                
            }
            return Response(json.dumps({"data": result}), status=200, mimetype='application/json')
        else:
                
            frappe.local.response.http_status_code = 401
            return json.loads(response.text)
            
            
    except Exception as e:
            # frappe.local.response.http_status_code = 401
            # return json.loads(response.text)
            return Response(json.dumps({"message": e , "user_count": 0}), status=500, mimetype='application/json')




@frappe.whitelist(allow_guest=True)
def generate_custom_token(username, password):  #Used for development testing only. not for production
    
    #this function can be used for development testing only. not for production. Uncomment the below code to use it.
    # return Response(json.dumps({"message": "Can not be used for production environmet" , "user_count": 0}), status=500, mimetype='application/json')
    #------------
    
    try:
        clientID, clientSecret, clientUser = frappe.db.get_value('OAuth Client', {'app_name': 'MobileAPP'}, ['client_id', 'client_secret','user'])
        client_id = clientID  # Replace with your OAuth client ID
        client_secret = clientSecret  # Replace with your OAuth client secret
        url =  frappe.local.conf.host_name  + "/api/method/employee_app.gauth.get_token"
        payload = {
            "username": username,
            "password": password,
            "grant_type": "password",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        files = []
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, files=files)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            frappe.local.response.http_status_code = 401
            return json.loads(response.text)
           
            
    except Exception as e:
            frappe.local.response.http_status_code = 401
            return json.loads(response.text)


            
@frappe.whitelist(allow_guest=True)
def generate_custom_token_for_employee( password):
    try:
        clientID, clientSecret, clientUser = frappe.db.get_value('OAuth Client', {'app_name': 'MobileAPP'}, ['client_id', 'client_secret','user'])
        username = clientUser
       
        client_id = clientID  # Replace with your OAuth client ID
        client_secret = clientSecret  # Replace with your OAuth client secret
        url =  frappe.local.conf.host_name  + "/api/method/employee_app.gauth.get_token"
        payload = {
            # "username": username,
            "username": clientUser,
            "password": password,
            "grant_type": "password",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        files = []
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, data=payload, files=files)
        # return json.loads(response.text)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            frappe.local.response.http_status_code = 401
            return json.loads(response.text)
        
    except Exception as e:
     
        frappe.local.response.http_status_code = 401
        return json.loads(response.text)

@frappe.whitelist(allow_guest=True)
def whoami():
        try:
            
            # return {"data": "Guest"}
            response_content = {
                "data": 
                    {
                        "user": frappe.session.user,
                    }
            }
            return Response(json.dumps(response_content), status=404, mimetype='application/json')
            # return frappe.session.user
        except Exception as e:
             frappe.throw(error)

@frappe.whitelist()
def get_user_name(user_email = None, mobile_phone = None):
    if mobile_phone is not None:
        user_details = frappe.get_list('User', filters={'mobile_no': mobile_phone}, fields=["name", "enabled"] )
    elif user_email is not None:
        user_details = frappe.get_list('User', filters={'email': user_email}, fields=["name", "enabled"] )
    else:
        return  Response(json.dumps({"data": "User not found" , "user_count": 0}), status=404, mimetype='application/json')
    
    if len(user_details) >=1:
        return  Response(json.dumps({"data":user_details , "user_count": 0}), status=200, mimetype='application/json')

    else:
        return  Response(json.dumps({"data": "User not found" , "user_count": 0}), status=404, mimetype='application/json')

def check_user_name(user_email = None, mobile_phone = None,user_name=None):
    if mobile_phone is not None:
        user_details_mobile = frappe.get_list('User', filters={'mobile_no': mobile_phone}, fields=["name", "enabled"] )
    if user_email is not None:
        user_details_email = frappe.get_list('User', filters={'email': user_email}, fields=["name", "enabled"] )
    if user_name is not None:
        user_details_user_name = frappe.get_list('User', filters={'username':user_name}, fields=["name", "enabled"] )
    if len(user_details_mobile) >=1 or len(user_details_email) >=1 or len(user_details_user_name)>=1:
        return  1
    else:
        return  0

             
@frappe.whitelist()
def is_user_available(user_email = None, mobile_phone = None):
        # response = Response()
        try:
            if mobile_phone is not None:
                mobile_count = len(frappe.get_all('User', {'mobile_no': mobile_phone}))
            else:
                mobile_count = 0
                
            if user_email is not None:
                email_count = len(frappe.get_all('User', {'email': user_email}))
            else:
                email_count = 0
                
            if mobile_count >= 1 and email_count < 1:
                response = {"message": "Mobile exists", "user_count": mobile_count}
                status_code = 200
            if email_count >= 1 and mobile_count < 1:
                response = {"message": "Email exists", "user_count": email_count}
                status_code = 200
            if mobile_count >= 1 and email_count >= 1:
                response = {"message": "Mobile and Email exists", "user_count": mobile_count}
                status_code = 200
            if mobile_count < 1 and email_count < 1:
                response = {"message": "Mobile and Email does not exist", "user_count": 0}
                status_code = 404
            return Response(json.dumps(response), status=status_code, mimetype='application/json')

        except Exception as e:
                return  Response(json.dumps({"message": e , "user_count": 0}), status=500, mimetype='application/json')
            

@frappe.whitelist()
def g_create_user(full_name, password, mobile_no, email,qid, role=None):
    # Check if the user already exists
    if check_user_name(user_email=email, mobile_phone=mobile_no,user_name=full_name) > 0:
        return Response(json.dumps({"message": "User already exists", "user_count": 1}), status=409, mimetype='application/json')

    try:
        # Validate custom_qid length
        if not (qid.isdigit() and len(qid) == 11):
            raise ValueError("Invalid custom_qid. It should be exactly 11 digits.")

        # Create User document
        frappe.get_doc({
            "doctype": "User",
            "name": email,
            "first_name": full_name,
            "mobile_no": mobile_no,
            "email": email,
            "roles": [{"role": role}]
        }).insert()

        # Create Customer document
        frappe.get_doc({
            "doctype": "Customer",
            "name": email,
            "customer_name": email,
            "custom_user": email,
            "custom_full_name": full_name,
            "custom_mobile_number": mobile_no,
            "email": email,
            "custom_qid": qid
        }).insert()

        # Generate reset password key
        return g_generate_reset_password_key(email, send_email=False, password_expired=False, mobile=mobile_no)

    except ValueError as ve:
        return Response(json.dumps({"message": str(ve), "user_count": 0}), status=400, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({"message": str(e), "user_count": 0}), status=500, mimetype='application/json')


@frappe.whitelist()
def g_update_password(username, password):
    try:
        if(len(frappe.get_all('User', {'name': username}))<1):
            return  Response(json.dumps({"message": "User not found" , "user_count": 0}), status=404, mimetype='application/json')    
        
        _update_password(username, password, logout_all_sessions=True)
        qid=frappe.get_list("Customer", fields=["name as id","custom_full_name as  full_name","custom_mobile_number as phone","name as email","custom_qid as qid"], filters={'name': ['like', username]})
        result={
           "message": "Password successfully updated" ,
           "user_details":qid[0] if qid else {} 
        }
        # frappe.db.commit()
        return  Response(json.dumps({"data":result }), status=200, mimetype='application/json')
        
    except Exception as e:
        return  Response(json.dumps({"message": e , "user_count": 0}), status=500, mimetype='application/json')
    
@frappe.whitelist()
def g_generate_reset_password_key(user, mobile="", send_email=False, password_expired=False,):
    
    if  mobile=="" :
       return  Response(json.dumps({"message": "Mobile number not found" , "user_count": 0}), status=404, mimetype='application/json')   
    try:
        if(len(frappe.get_all('User', {'name': user}))<1):
            return  Response(json.dumps({"message": "User not found" , "user_count": 0}), status=404, mimetype='application/json')   
        key  = str(random.randint(100000, 999999))
        doc2 = frappe.get_doc("User", user)
        doc2.reset_password_key = key
        doc2.last_reset_password_key_generated_on = now_datetime()
        doc2.save()
        
        url = "/update-password?key=" + key
        if password_expired:
            url = "/update-password?key=" + key + "&password_expired=true"
        # send_sms_expertexting(mobile,key)  # stop this on testing cycle as it send SMSes
        send_sms_vodafone(mobile, urllib.parse.quote(f"Your Validation code for DallahMzad is {key} Thank You.  \n \n  رمز التحقق الخاص بك لـ DallahMzad هو {key} شكرًا لك."))
        link = get_url(url)
        if send_email:
            User.password_reset_mail(link)

        return   Response(json.dumps({"reset_key": key , "generated_time": str(now_datetime()), "URL": link }), status=200, mimetype='application/json')
    except Exception as e:
        return  Response(json.dumps({"message": e , "user_count": 0}), status=500, mimetype='application/json')

@frappe.whitelist()
def g_delete_user(id, email, mobile_no):
    try:
        if(len(frappe.get_all('User', {"name":id, "email": email, "mobile_no": mobile_no}))<1):
            return  Response(json.dumps({"message": "User not found" , "user_count": 0}), status=404, mimetype='application/json')    
        
        frappe.db.delete("User", {"name":id, "email": email, "mobile_no": mobile_no}),
        frappe.db.delete("Customer", {"name":id, "customer_name": email, "custom_mobile_number": mobile_no})
        return  Response(json.dumps({"message": "User successfully deleted" , "user_count": 1}), status=200, mimetype='application/json')
        
    except Exception as e:
        return  Response(json.dumps({"message": e , "user_count": 0}), status=500, mimetype='application/json')


@frappe.whitelist()
def g_user_enable(username, email, mobile_no, enable_user: bool = True):
    try:
        if(len(frappe.get_all('User', {"name":username, "email": email, "mobile_no": mobile_no}))<1):
            return  Response(json.dumps({"message": "User not found" , "user_count": 0}), status=404, mimetype='application/json')    

        frappe.db.set_value('User', username, 'enabled', enable_user)
        return  Response(json.dumps({"message": f"User successfully {'enabled' if enable_user else 'disabled'} " , "user_count": 1}), status=200, mimetype='application/json')
       
    except Exception as e:
        return  Response(json.dumps({"message": e , "user_count": 0}), status=500, mimetype='application/json')

def get_number_of_files(file_storage):
    # Implement your logic to count the number of files
    # Adjust this based on the actual structure of the FileStorage object
    # For example, if FileStorage has a method to get the number of files, use that

    # Example: Assuming a method called get_num_files() on FileStorage
    if hasattr(file_storage, 'get_num_files') and callable(file_storage.get_num_files):
        return file_storage.get_num_files()
    else:
        return 0  # Default to 0 if no specific method or attribute is available

@frappe.whitelist(allow_guest=True)
def time():
    server_time = frappe.utils.now()
    unix_time = frappe.utils.get_datetime(frappe.utils.now_datetime()).timestamp()
    api_response = {
        "data": {
            "serverTime": server_time,
            "unix_time": unix_time
        }
    }
    return api_response


@frappe.whitelist(allow_guest=True)
def upload_file():
    
    user = None
    if frappe.session.user == "Guest":
        if frappe.get_system_settings("allow_guests_to_upload_files"):
            ignore_permissions = True
        else:
            raise frappe.PermissionError
    else:
        user: "User" = frappe.get_doc("User", frappe.session.user)
        ignore_permissions = False


    files = frappe.request.files
    file_names = []
    urls = []
    # filecount = 0
    # for key, file in files.items():
    #     filecount = filecount + 1
    #     file_names.append(key)


    # return file_names
    
    
    is_private = frappe.form_dict.is_private
    doctype = frappe.form_dict.doctype
    docname = frappe.form_dict.docname
    fieldname = frappe.form_dict.fieldname
    file_url = frappe.form_dict.file_url
    folder = frappe.form_dict.folder or "Home"
    method = frappe.form_dict.method
    filename = frappe.form_dict.file_name
    optimize = frappe.form_dict.optimize
    content = None
    filenumber = 0
    for key,file in files.items():
                        filenumber = filenumber + 1
                        file_names.append(key)
                        file = files[key]
                        content = file.stream.read()
                        filename = file.filename

                        content_type = guess_type(filename)[0]
                        if optimize and content_type and content_type.startswith("image/"):
                            args = {"content": content, "content_type": content_type}
                            if frappe.form_dict.max_width:
                                args["max_width"] = int(frappe.form_dict.max_width)
                            if frappe.form_dict.max_height:
                                args["max_height"] = int(frappe.form_dict.max_height)
                            content = optimize_image(**args)

                        frappe.local.uploaded_file = content
                        frappe.local.uploaded_filename = filename

                        if content is not None and (
                            frappe.session.user == "Guest" or (user and not user.has_desk_access())
                        ):
                            filetype = guess_type(filename)[0]
                            # if filetype not in ALLOWED_MIMETYPES:
                            #     frappe.throw(_("You can only upload JPG, PNG, PDF, TXT or Microsoft documents."))

                        if method:
                            method = frappe.get_attr(method)
                            is_whitelisted(method)
                            return method()
                        else:
                            # return frappe.get_doc(
                            doc = frappe.get_doc(
                                {
                                    "doctype": "File",
                                    "attached_to_doctype": doctype,
                                    "attached_to_name": docname,
                                    "attached_to_field": fieldname,
                                    "folder": folder,
                                    "file_name": filename,
                                    "file_url": file_url,
                                    "is_private": cint(is_private),
                                    "content": content,
                                }
                            ).save(ignore_permissions=ignore_permissions)
                            urls.append(doc.file_url)
                        
                            if fieldname is not None:
                                attach_field = frappe.get_doc(doctype, docname) #.save(ignore_permissions = True)
                                setattr(attach_field, fieldname, doc.file_url)
                                attach_field.save(ignore_permissions = True)
                            
                                
    return urls

@frappe.whitelist(allow_guest=True)
def send_sms_expertexting(phone_number,otp):  # Send SMS using experttexting.com
    try:
        phone_number = "+974" + phone_number
        url = "https://www.experttexting.com/ExptRestApi/sms/json/Message/Send"
        message_text = urllib.parse.quote(f"Your validation code for DallahMzad is {otp} Thank You.  \n \n  رمز التحقق الخاص بك لـ DallahMzad هو {otp} شكرًا لك.")
        # payload = f'username={get_sms_id("experttexting")}&from=DEFAULT&to={phone_number}&text=Your%20validation%20code%20for%20DallahMzad%20is%20{otp}%20Thank%20You.'
        payload = f'username={get_sms_id("experttexting")}&from=DEFAULT&to={phone_number}&text={message_text}&type=unicode'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code  in (200,201 ):
            return True
        else:
            return False
        
        
    except Exception as e:
        return "Error in qr sending SMS   " + str(e) 


@frappe.whitelist(allow_guest=True)
def send_sms_vodafone(phone_number, message_text):  # send sms through Vodafone Qatar
    try:
        
        
            phone_number = "+974" + phone_number
            url = "https://connectsms.vodafone.com.qa/SMSConnect/SendServlet"
            # message_text = urllib.parse.quote(f"Your validation code for DallahMzad is {otp} Thank You.  \n \n  رمز التحقق الخاص بك لـ DallahMzad هو {otp} شكرًا لك.")
            # payload = f'username={get_sms_id("experttexting")}&from=DEFAULT&to={phone_number}&text=Your%20validation%20code%20for%20DallahMzad%20is%20{otp}%20Thank%20You.'
            payload = get_sms_id("vodafone") + "&content=" + message_text + "&source=97401" + "&destination=" + phone_number
            headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("GET", url + payload, headers=headers, data="")
            # return url + payload
            if response.status_code  in (200,201 ):
                return True
            else:
                return False
        
        
    except Exception as e:
        return "Error in qr sending SMS   " + str(e) 



@frappe.whitelist(allow_guest=True)
def send_sms_twilio(phone_number,otp):  # Send SMS OTP using twilio
    # success response = 201 created
    try:
        import requests
        phone_number = "+974" + phone_number
        parts = get_sms_id('twilio').split(":")

        url = f"https://api.twilio.com/2010-04-01/Accounts/{parts[0]}/Messages.json"
        payload = f'To={phone_number}&From=+18789999387&Body=Your%20DallahMzad%OTP Verification code%20%20is%20{otp}%20Please%20use%20it%20on%20the%20site%20or%20App'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {parts[1]}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code  in (200,201 ):
            return True
        else:
            return response.text
         
        # if response.status_code  in (400,405,406,409 ):
        
    except Exception as e:
        return "Error in qr sending SMS   " + str(e)

@frappe.whitelist(allow_guest=True)
def payment_gateway_log(reference,amount,user,bid):
                    try:
                        current_time = frappe.utils.now()
                        frappe.get_doc({
                            "doctype": "payment_gateway_initiated",
                            "reference": reference,
                            "date_time": current_time,
                            "amount": amount,
                            "user": user,
                            "bid": bid
                        }).insert(ignore_permissions=True)
                        return "Successfully logged Payment gateway initialization"
                    except Exception as e:
                        frappe.log_error(title='Payment logging failed',message=frappe.get_traceback())
                        return "Error in payment gateway log  " + str(e)
                    

def get_sms_id(provider):
    default_company = frappe.db.get_single_value("Global Defaults", "default_company")
    if provider == "twilio":
        return frappe.db.get_value("Company", default_company, "custom_twilio_id")
    if provider == "experttexting":
        return frappe.db.get_value("Company", default_company, "custom_experttexting_id")
    if provider == "vodafone":
        app = frappe.db.get_value("Company", default_company, "custom_vodafone_application")
        passw = frappe.db.get_value("Company", default_company, "custom_vodafone_password")
        mask = frappe.db.get_value("Company", default_company, "custom_vodafone_mask")
        param_string = "?application=" + app + "&password=" + passw + "&mask=" + mask 
        return param_string

    

@frappe.whitelist(allow_guest=True)
def make_payment_entry(
	amount,
    user,
	bid,
    reference
):

    if amount == 0:
        return "Amount not correct"

    journal_entry = frappe.new_doc("Journal Entry")
    journal_entry.posting_date = frappe.utils.now()
    journal_entry.company = frappe.db.get_single_value("Global Defaults", "default_company")
    journal_entry.voucher_type = "Journal Entry"
    reference = reference + "  dated:  " + str(now_datetime())  + " Bid/Other document No: " + bid
    journal_entry.remark = reference
    debit_entry = {
        # "account": "QIB Account - D",
        "account": "1310 - Debtors - D",
        "credit": amount,
        "credit_in_account_currency": amount,
        "account_currency": "QAR",
        "reference_name": "",
        "reference_type": "",
        "reference_detail_no": "",
        "cost_center": "",
        "project": "",
        "party_type": "Customer",
        "party": user,
        "is_advance": 0,
        "reference_detail_no": reference
    }

    credit_entry = {
        "account": "QIB Account - D",
        # "account": "1310 - Debtors - D",
        "debit": amount,
        "debit_in_account_currency": amount,
        "account_currency": "QAR",
        "reference_name": "",
        "reference_type": "",
        "reference_detail_no": "",
        "cost_center": "",
        "project": "",
        "reference_detail_no": reference
        # "party_type": "Customer",
        # "party": "mumtaz@erpgulf.com422"
        
    }

	# for dimension in get_accounting_dimensions():
	# 	debit_entry.update({dimension: item.get(dimension)})

	# 	credit_entry.update({dimension: item.get(dimension)})

    journal_entry.append("accounts", debit_entry)
    journal_entry.append("accounts", credit_entry)

    try:
            # a=10
            journal_entry.save(ignore_permissions=True)
            journal_entry.submit()
            # if submit:
            # journal_entry.submit()

            # frappe.db.commit()
            return  Response(json.dumps({"data": "JV Successfully created ", "message": "" }), status=200, mimetype='application/json')
    except Exception as e:
            frappe.db.rollback()
            frappe.log_error(title='Payment Entry failed to JV',message=frappe.get_traceback())
            frappe.flags.deferred_accounting_error = True
            return str(e)
            # return  Response(json.dumps({"data": "There was an error in creating JV", "message": "Use token with higher privilage to enter JV" }), status=401, mimetype='application/json')
        


@frappe.whitelist()
def get_customer_details(user_email = None, mobile_phone = None):
    if mobile_phone is not None:
        customer_details = frappe.get_list('Customer', filters={'custom_mobile_number': mobile_phone}, fields=["name as email", "enabled","custom_full_name as full_name","custom_mobile_number as mobile_number","custom_qid as qid"] )
    elif user_email is not None:
        customer_details = frappe.get_list('Customer', filters={'name': user_email}, fields=["name as email", "enabled","custom_full_name as full_name","custom_mobile_number as mobile_number","custom_qid as qid"] )
    else:
        return  Response(json.dumps({"message": "Customer not found" , "user_count": 0}), status=404, mimetype='application/json')
    
    if len(customer_details) >=1:
        return  customer_details
    else:
        return  Response(json.dumps({"message": "Customer not found" , "user_count": 0}), status=404, mimetype='application/json')
    
def _get_customer_details(user_email = None, mobile_phone = None):
    if mobile_phone is not None:
        customer_details = frappe.get_list('Customer', filters={'custom_mobile_number': mobile_phone}, fields=["name as email", "enabled","custom_full_name as full_name","custom_mobile_number as mobile_number","custom_qid as qid"] )
    elif user_email is not None:
        customer_details = frappe.get_list('Customer', filters={'name': user_email}, fields=["name as email", "enabled","custom_full_name as full_name","custom_mobile_number as mobile_number","custom_qid as qid"] )
    else:
        return  Response(json.dumps({"message": "Customer not found" , "user_count": 0}), status=404, mimetype='application/json')
    
    if len(customer_details) >=1:
        return  customer_details[0]['email'], customer_details[0]['full_name'], customer_details[0]['mobile_number'], customer_details[0]['qid']
    else:
        return  Response(json.dumps({"message": "Customer not found" , "user_count": 0}), status=404, mimetype='application/json')
    
@frappe.whitelist(allow_guest=True)
def get_account_balance(customer=None):
    response_content =frappe.session.user
    balance=  get_balance_on(party_type="Customer", party=response_content)
    result={
        "balance": 0-balance
    }
    return  Response(json.dumps({"data":result}), status=200, mimetype='application/json')
@frappe.whitelist(allow_guest=True)

def create_refresh_token(refresh_token):
    url =  frappe.local.conf.host_name  + "/api/method/frappe.integrations.oauth2.get_token"
    payload = f'grant_type=refresh_token&refresh_token={refresh_token}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    files = []
    
    response = requests.post(url, headers=headers, data=payload, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Parse the JSON string in the response message
            message_json = json.loads(response.text)
            
            # Create the new message format
            new_message = {
                "access_token": message_json["access_token"],
                "expires_in": message_json["expires_in"],
                "token_type": message_json["token_type"],
                "scope": message_json["scope"],
                "refresh_token": message_json["refresh_token"]
            }

            # Return the new message format directly
            return  Response(json.dumps({"data": new_message}), status=200, mimetype='application/json')
        except json.JSONDecodeError as e:
            return  Response(json.dumps({"data": f"Error decoding JSON: {e}"}), status=401, mimetype='application/json')
    else:
        # If the request was not successful, return the original response text
        return  Response(json.dumps({"data": response.text}), status=401, mimetype='application/json')


@frappe.whitelist(allow_guest=True)
def test_redirect_url():
    redirect_url = "https://doodles.google/search/"
    
    response_data = {
        'data': 'Redirecting to here',
        'redirect_url': redirect_url
    }
    
    # return {
    #     'status': 'redirect',
    #     'location': "https://doodles.google/search/"
    return  Response(json.dumps(response_data), status=303, mimetype='text/html; charset=utf-8')
    
    # }
    

    



@frappe.whitelist()
def g_update_password_using_usertoken(password):
    try:
        username =frappe.session.user
        if(len(frappe.get_all('User', {'name': username}))<1):
            return  Response(json.dumps({"message": "User not found" , "user_count": 0}), status=404, mimetype='application/json')    
        
        _update_password(username, password, logout_all_sessions=True)
        qid=frappe.get_list("Customer", fields=["name as id","custom_full_name as  full_name","custom_mobile_number as phone","name as email","custom_qid as qid"], filters={'name': ['like', username]})
        result={
           "message": "Password successfully updated" ,
           "user_details":qid[0] if qid else {} 
        }
        # frappe.db.commit()
        return  Response(json.dumps({"data":result }), status=200, mimetype='application/json')
        
    except Exception as e:
        return  Response(json.dumps({"message": e , "user_count": 0}), status=500, mimetype='application/json')

            
@frappe.whitelist(allow_guest=True)
def g_update_password_using_reset_key(new_password,reset_key,username):
    try:
        
        if(len(frappe.get_all('User', {'name': username}))<1):
            return  Response(json.dumps({"message": "User not found" , "user_count": 0}), status=404, mimetype='application/json')  
        
        res =  _update_password_reset_key(new_password=new_password, key=reset_key)
        # if res.get("message"):
        # return  frappe.local.response.http_status_code
        if frappe.local.response.http_status_code == 410:
            return  Response(json.dumps({"message": "Reset key not valid or expired"  , "user_count": 0}), status=401, mimetype='application/json')
        # return res["message"]
	    
        
        
        qid=frappe.get_list("Customer", fields=["name as id","custom_full_name as  full_name","custom_mobile_number as phone","name as email","custom_qid as qid"], filters={'name': ['like', username]})
        result={
           "message": "Password successfully updated" ,
           "user_details":qid[0] if qid else {} 
        }
        # frappe.db.commit()
        return  Response(json.dumps({"data":result }), status=200, mimetype='application/json')
        
    except Exception as e:
        return  Response(json.dumps({"message": e , "user_count": 0}), status=500, mimetype='application/json')


@frappe.whitelist(allow_guest=False)
def send_firebase_notification(title,body,client_token="",topic=""):
    #Sending firebase notification to Android and IPhone from Frappe ERPNext 
    
    
    import firebase_admin
    from firebase_admin import credentials,exceptions,messaging

    if client_token == "" and topic == "":
            return  Response(json.dumps({"message": "Please provide either client token or topic to send message to Firebase" , "message_sent": 0}), status=417, mimetype='application/json')
    try:
        # Check if app already exists
        try:
            firebase_admin.get_app()
        except ValueError:
            # If not, then initialize it
            cred = credentials.Certificate("firebase.json")
            firebase_admin.initialize_app(cred)
        
        if client_token != "":
            message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=client_token,
            )
            
        if topic != "":
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                topic=topic,
            )
        return {'message': 'Successfully sent message', 'response': messaging.send(message)}
    except Exception as e:
        error_message = str(e)
        frappe.response['message'] = 'Failed to send firebase message'
        frappe.response['error'] = error_message
        frappe.response['http_status_code'] = 500
        return frappe.response
    
def _get_access_token():
    
            """Retrieve a valid access token that can be used to authorize requests. FCM 

            :return: Access token.
            """
            import google.auth.transport.requests
            from google.oauth2 import service_account
            SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']
            credentials = service_account.Credentials.from_service_account_file(
                'dallah-fcm.json', scopes=SCOPES)
            request = google.auth.transport.requests.Request()
            credentials.refresh(request)
            return credentials.token

@frappe.whitelist(allow_guest=False)
def send_firebase_data(auction_id,notification_type,user_name=None,user_id=None,winner_amount=None,client_token="",topic="",):
    #Sending firebase data to Android and IPhone from Frappe ERPNext 
                        
                    import requests
                    import json
                    # frappe.throw(str(_get_access_token()))
                    url = "https://fcm.googleapis.com/v1/projects/dallah-424a0/messages:send"
                    
                    if notification_type=="auction_ended":
                            payload = json.dumps({
                            "message": {
                                "topic": auction_id, #auctionId: subcriber to that auction id,
                                "data": {
                                    "notification_type": "auction_ended",
                                    "auctionId": auction_id # ////auctionId
                                }
                            }
                            })
                    else:
                            # frappe.throw(str(winner_amount))
                            payload = json.dumps({
                            "message": {
                                "topic": auction_id,
                                "data": {
                                    "notification_type": "winner_announcement",
                                    "auctionId": auction_id,
                                    "winner_name": user_id,
                                    "winner_id": user_id,
                                    "highest_bid_amount":"{:,.2f}".format(winner_amount)
                                }
                            }
                            })
                        
                    headers = {
                        'Authorization': 'Bearer ' + _get_access_token(),
                        'Content-Type': 'application/json',
                    }

                    response = requests.request("POST", url, headers=headers, data=payload)
                    return Response(json.dumps({"data": "Message sent"}), status=200, mimetype='application/json')

        
@frappe.whitelist(allow_guest=False)
def firebase_subscribe_to_topic(topic,fcm_token):
            import firebase_admin
            from firebase_admin import credentials, messaging

            if fcm_token == "" and topic == "":
                return  Response(json.dumps({"message": "Please provide FCM Token and  topic to send message to Firebase" , "message_sent": 0}), status=417, mimetype='application/json')
        
            try:

                    # Check if app already exists
                    try:
                        firebase_admin.get_app()
                    except ValueError:
                        # If not, then initialize it
                        cred = credentials.Certificate("firebase.json")
                        firebase_admin.initialize_app(cred)
                        
                    try:
                        response = messaging.subscribe_to_topic(fcm_token, topic)
                        if response.failure_count > 0:
                            return  Response(json.dumps({"data":"Failed to subscribe to Firebase topic"}), status=400, mimetype='application/json')
                        else:
                            return  Response(json.dumps({"data":"Successfully subscribed to Firebase topic"}), status=200, mimetype='application/json')
                    except Exception as e:
                        return  Response(json.dumps({"data":"Error happened while trying to  subscribe to Firebase topic"}), status=400, mimetype='application/json')

                    
            except Exception as e:
                    error_message = str(e)
                    frappe.response['message'] = 'Failed to send firebase message'
                    frappe.response['error'] = error_message
                    frappe.response['http_status_code'] = 500
                    return frappe.response



@frappe.whitelist(allow_guest=True) 
def send_email(Subject=None, Text=None, To=None, From=None):
    url = "https://api.sparkpost.com/api/v1/transmissions"
    
    
    if not To:
        return Response(json.dumps({"message": "At least one valid recipient is required"}), status=404, mimetype='application/json')
    if not Text:
        return Response(json.dumps({"message": "At least one of text or html needs to exist in content"}), status=404, mimetype='application/json')
    if not Subject:
        return Response(json.dumps({"message": "subject is a required field"}), status=404, mimetype='application/json')
    if not From:
        return Response(json.dumps({"message": "from is a required field"}), status=404, mimetype='application/json')
    company=frappe.get_doc("Company","DallahMzad")
    api_key=company.custom_sparkpost_id
    # return api_key
    try:
        payload = json.dumps({
            "content": {
                "from": From,
                "subject": Subject,
                "text": Text
            },
            "recipients": [
                {
                    "address": To
                }
            ]
        })
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        
        
        if response.status_code == 200:
            return Response(response.text, status=200, mimetype='application/json')
        else:
            
            return Response(response.text, status=response.status_code, mimetype='application/json')
    
    except Exception as e:
        
        return Response(json.dumps({"message": str(e)}), status=500, mimetype='application/json')

@frappe.whitelist(allow_guest=True) 
def login_time():
    username =frappe.session.user
    doc=frappe.get_all("log_in details",fields=["time"], filters={'user': ['like',username]})
    return doc