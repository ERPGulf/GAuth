import requests
import json
import frappe
import json
import base64
from frappe.utils.image import optimize_image
import os
from frappe.utils import cint
from mimetypes import guess_type
from typing import TYPE_CHECKING
from werkzeug.wrappers import Response
from frappe.utils.password import update_password as _update_password
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
            return json.loads(response.text)
        else:
            frappe.local.response.http_status_code = 401
            return json.loads(response.text)
            
    except Exception as e:
            # frappe.local.response.http_status_code = 401
            # return json.loads(response.text)
            return Response(json.dumps({"message": e , "user_count": 0}), status=500, mimetype='application/json')
        
        
        
@frappe.whitelist(allow_guest=True)
def generate_token_secure_for_users( username, password, app_key):
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
        if response.status_code == 200:
            response_data = json.loads(response.text)
            response_data['Email'],response_data['Full_name'], response_data['Phone_number'],response_data['QID'] = _get_customer_details(user_email=username)      
            return response_data
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
    return Response(json.dumps({"message": "Can not be used for production environmet" , "user_count": 0}), status=500, mimetype='application/json')
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
            return frappe.session.user
        except Exception as e:
             frappe.throw(error)

@frappe.whitelist()
def get_user_name(user_email = None, mobile_phone = None):
    if mobile_phone is not None:
        user_details = frappe.get_list('User', filters={'mobile_no': mobile_phone}, fields=["name", "enabled"] )
    elif user_email is not None:
        user_details = frappe.get_list('User', filters={'email': user_email}, fields=["name", "enabled"] )
    else:
        return  Response(json.dumps({"message": "User not found" , "user_count": 0}), status=404, mimetype='application/json')
    
    if len(user_details) >=1:
        return  user_details
    else:
        return  Response(json.dumps({"message": "User not found" , "user_count": 0}), status=404, mimetype='application/json')

def check_user_name(user_email = None, mobile_phone = None):
    if mobile_phone is not None:
        user_details_mobile = frappe.get_list('User', filters={'mobile_no': mobile_phone}, fields=["name", "enabled"] )
    if user_email is not None:
        user_details_email = frappe.get_list('User', filters={'email': user_email}, fields=["name", "enabled"] )
    if len(user_details_mobile) >=1 or len(user_details_email) >=1:
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
def g_create_user(full_name, password, mobile_no, email, id,role=None):
    # return "inside g_create_user"
    # return check_user_name(user_email=email, mobile_phone=mobile_no)
    if(check_user_name(user_email=email, mobile_phone=mobile_no)>0):
        return  Response(json.dumps({"message": "User already exists" , "user_count": 1}), status=409, mimetype='application/json')
    
    try:
        frappe.get_doc({"doctype":"User",
                        "name":email,
                        "first_name":full_name,
                        "mobile_no":mobile_no,
                        "email": email,
                        "roles": [{"role": role}]
                        }).insert()
        
        frappe.get_doc({"doctype":"Customer",
                        "name":email,
                        "customer_name": email,
                        "custom_user": email,
                        "custom_full_name":full_name,
                        "custom_mobile_number":mobile_no,
                        "email": email,
                        "custom_qid": id,
                        }).insert()
        
        
        return g_generate_reset_password_key(email, send_email=False, password_expired=False)

        # return  Response(json.dumps({"message": "User successfully created" , "user_count": 1}), status=200, mimetype='application/json')
        
    except Exception as e:
        return  Response(json.dumps({"message": e , "user_count": 0}), status=500, mimetype='application/json')
    

@frappe.whitelist()
def g_update_password(username, password):
    try:
        if(len(frappe.get_all('User', {'name': username}))<1):
            return  Response(json.dumps({"message": "User not found" , "user_count": 0}), status=404, mimetype='application/json')    
        
        _update_password(username, password, logout_all_sessions=True)
        # frappe.db.commit()
        return  Response(json.dumps({"message": "Password successfully updated" , "user_count": 1}), status=200, mimetype='application/json')
        
    except Exception as e:
        return  Response(json.dumps({"message": e , "user_count": 0}), status=500, mimetype='application/json')
    
@frappe.whitelist()
def g_generate_reset_password_key(user, send_email=False, password_expired=False):
    try:
        key  = str(random.randint(100000, 999999))
        doc2 = frappe.get_doc("User", user)
        doc2.reset_password_key = key
        doc2.last_reset_password_key_generated_on = now_datetime()
        doc2.save()
        
        url = "/update-password?key=" + key
        if password_expired:
            url = "/update-password?key=" + key + "&password_expired=true"

        link = get_url(url)
        if send_email:
            User.password_reset_mail(link)

        return   Response(json.dumps({"reset_key": key , "generated_time": str(now_datetime()), "URL": link }), status=200, mimetype='application/json')
    except Exception as e:
        return  Response(json.dumps({"message": e , "user_count": 0}), status=500, mimetype='application/json')

@frappe.whitelist()
def g_delete_user(username, email, mobile_no):
    try:
        if(len(frappe.get_all('User', {"name":username, "email": email, "mobile_no": mobile_no}))<1):
            return  Response(json.dumps({"message": "User not found" , "user_count": 0}), status=404, mimetype='application/json')    
        
        frappe.db.delete("User", {"name":username, "email": email, "mobile_no": mobile_no}),
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
def send_sms_expertexting(phone_number,otp):
    try:
        phone_number = "+974" + phone_number
        url = "https://www.experttexting.com/ExptRestApi/sms/json/Message/Send"

        payload = f'username={get_sms_id("experttexting")}&from=DEFAULT&to={phone_number}&text=Your%20validation%20code%20for%20DallahMzad%20is%20{otp}%20Thank%20You.'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code  in (200,201 ):
            return True
        else:
            return False
        
        
    except Exception as e:
        frappe.throw("Error in qr sending SMS   " + str(e))   


@frappe.whitelist(allow_guest=True)
def send_sms_twilio(phone_number,otp):
    # success response = 201 created
    try:
        import requests
        phone_number = "+974" + phone_number
        parts = get_sms_id('twilio').split(":")

        url = f"https://api.twilio.com/2010-04-01/Accounts/{parts[0]}/Messages.json"
        payload = f'To={phone_number}&From=+18789999387&Body=Your%20DallahMzad%20Validation%20%20is%20{otp}%20Please%20use%20it%20on%20the%20site%20or%20App'
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

	debit_entry = {
		"account": "QIB Account - D",
		"credit": amount,
		"credit_in_account_currency": amount,
		"account_currency": "QAR",
		"reference_name": None,
		"reference_type": "Journal Entry",
		"reference_detail_no": "",
		"cost_center": "",
		"project": "",
	}

	credit_entry = {
		"account": "1310 - Debtors - D",
		"debit": amount,
		"debit_in_account_currency": amount,
		"account_currency": "QAR",
		"reference_name": None,
		"reference_type": "Journal Entry",
		"reference_detail_no": "",
		"cost_center": "",
		"project": "",
	}

	# for dimension in get_accounting_dimensions():
	# 	debit_entry.update({dimension: item.get(dimension)})

	# 	credit_entry.update({dimension: item.get(dimension)})

	journal_entry.append("accounts", debit_entry)
	journal_entry.append("accounts", credit_entry)

	try:
		journal_entry.save(ignore_permissions=True)

		# if submit:
		# 	journal_entry.submit()

		frappe.db.commit()
	except Exception as e:
            frappe.db.rollback()
            frappe.log_error(title='Payment Entry failed to JV',message=frappe.get_traceback())
            frappe.flags.deferred_accounting_error = True
            return  Response(json.dumps({"data": "null", "message": str(e) }), status=400, mimetype='application/json')

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
def get_account_balance(customer):
    return  get_balance_on(party_type="Customer", party=customer)

    