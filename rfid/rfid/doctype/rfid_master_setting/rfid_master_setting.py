# Copyright (c) 2023, soham.pawar@erpdata.in and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RFIDMasterSetting(Document):
    pass
	# @frappe.whitelist()
	# def get_user(self):
	# 	self.rfid_operator_name = frappe.db.get_value("User", frappe.session.user, "full_name")
	# 	self.rfid_operator_id= frappe.session.user

