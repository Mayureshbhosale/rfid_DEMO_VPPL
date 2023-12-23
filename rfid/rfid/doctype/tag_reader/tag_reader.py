# myapp/myapp/doctype/tag_reader/tag_reader.py

import frappe
from frappe.model.document import Document


class TagReader(Document):

    @frappe.whitelist()
    def get_rfid_info(self):
        if not self.reader_name:
            self.username = frappe.db.get_value("User", frappe.session.user, "full_name")
            doc = frappe.get_all("RFID Master Setting",
                    fields=["rfid_machine", "idx", "date"],
                    filters={'rfid_operator_id': frappe.session.user},
                    order_by="date desc",
                    limit=1)

            for d in doc:
                self.reader_name = d.rfid_machine
                break

            rfidstatus = frappe.get_doc("Rfid tag Reading", "rfid-tag-reading")

            # Map RFID reader names to their corresponding status attributes
            reader_status_map = {
                "RFID 1": rfidstatus.rfid1_status,
                "RFID 2": rfidstatus.rfid2_status,
                "RFID 3": rfidstatus.rfid3_status
            }

            # Get the status based on the reader name
            temp = reader_status_map.get(self.reader_name)

            if temp is not None:
                # Display the status message with the appropriate indicator
                if temp == "Connected.":
                    frappe.msgprint((self.reader_name + ' : ' + temp), indicator="green", title="RFID Status")
                else:
                    frappe.msgprint((self.reader_name + ' : ' + temp), indicator="red", title="RFID Status")
            else:
                frappe.throw("User does not have any permission to access any RFID")

            

        # temp1=rfidstatus.rfid1_status
        # temp2=rfidstatus.rfid2_status
        # temp3=rfidstatus.rfid3_status
        # if temp1=="Connected.":
        #     temp=temp1
        #     if self.reader_name=="RFID 1":
        #         temp=rfidstatus.rfid1_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="green",title="RFID Status")
        #     if self.reader_name=="RFID 2":
        #         temp=rfidstatus.rfid2_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="green",title="RFID Status")
        #     if self.reader_name=="RFID 3":
        #         temp=rfidstatus.rfid3_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="green",title="RFID Status")
        # else:
        #     if self.reader_name=="RFID 1":
        #         temp=rfidstatus.rfid1_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="red",title="RFID Status")
        #     if self.reader_name=="RFID 2":
        #         temp=rfidstatus.rfid2_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="red",title="RFID Status")
        #     if self.reader_name=="RFID 3":
        #         temp=rfidstatus.rfid3_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="red",title="RFID Status")  
                 
        # if temp2=="Connected.":
        #     temp=temp2
        #     if self.reader_name=="RFID 1":
        #         temp=rfidstatus.rfid1_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="green",title="RFID Status")
        #     if self.reader_name=="RFID 2":
        #         temp=rfidstatus.rfid2_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="green",title="RFID Status")
        #     if self.reader_name=="RFID 3":
        #         temp=rfidstatus.rfid3_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="green",title="RFID Status")
        # else:
        #     if self.reader_name=="RFID 1":
        #         temp=rfidstatus.rfid1_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="red",title="RFID Status")
        #     if self.reader_name=="RFID 2":
        #         temp=rfidstatus.rfid2_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="red",title="RFID Status")
        #     if self.reader_name=="RFID 3":
        #         temp=rfidstatus.rfid3_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="red",title="RFID Status")   
                
        # if temp3=="Connected.":
        #     temp=temp3
        #     if self.reader_name=="RFID 1":
        #         temp=rfidstatus.rfid1_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="green",title="RFID Status")
        #     if self.reader_name=="RFID 2":
        #         temp=rfidstatus.rfid2_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="green",title="RFID Status")
        #     if self.reader_name=="RFID 3":
        #         temp=rfidstatus.rfid3_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="green",title="RFID Status")
        # else:
        #     if self.reader_name=="RFID 1":
        #         temp=rfidstatus.rfid1_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="red",title="RFID Status")
        #     if self.reader_name=="RFID 2":
        #         temp=rfidstatus.rfid2_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="red",title="RFID Status")
        #     if self.reader_name=="RFID 3":
        #         temp=rfidstatus.rfid3_status
        #         frappe.msgprint((self.reader_name+' : '+temp),indicator="red",title="RFID Status")        
                           
    @frappe.whitelist()
    def get_rfid(self):
        if not self.token_number:
            doc=frappe.get_doc("Rfid tag Reading")
            if self.reader_name=="RFID 1":
                self.token_number=doc.rfid_1
                self.validate_token_number()
            if self.reader_name=="RFID 2":
                self.token_number=doc.rfid_2
                self.validate_token_number()
            if self.reader_name=="RFID 3":
                self.token_number=doc.rfid_3
                self.validate_token_number()
        
   
    @frappe.whitelist()
    def before_save(self):
        self.assign_tag_value()
                 
    @frappe.whitelist()
    def assign_tag_value(self):
        transporter = self.get('transportar')
        h_and_t_transporter = frappe.db.get_value("H and T Contract", transporter, ['name'])
        if transporter == h_and_t_transporter:
            frappe.db.set_value("H and T Contract", h_and_t_transporter, 'rfid_tag', self.token_number)
        
        
    @frappe.whitelist()
    def validate_transporter(self):
        transportar=frappe.get_all('Tag Reader',filters={"transportar":self.transportar},fields=['name','transportar','transporter_name','token_number'])
        if transportar:
            frappe.throw(f'This {transportar[0].token_number} tag is Already assigned to <a href="{transportar[0].name}">Transporter {transportar[0].transportar}  {transportar[0].transporter_name}</a>')
       
            
        
            
    @frappe.whitelist()
    def validate_token_number(self):
        token_number=frappe.get_all('Tag Reader',filters={"token_number":self.token_number},fields=['name','token_number','transporter_name','transportar'])
        if token_number:
            frappe.throw(f'{token_number[0].token_number} tag is Already assigned to <a href="{token_number[0].name}">Transporter {token_number[0].transportar} {token_number[0].transporter_name}</a>')
            
            
    @frappe.whitelist()
    def ischecked(self):
        if self.delete_if_already_assign:
            transporter=frappe.get_all('Tag Reader',filters={"transportar":self.transportar},fields=['name'])
            for t in transporter:
                doc=frappe.get_doc("Tag Reader",t.name)
                doc.delete()