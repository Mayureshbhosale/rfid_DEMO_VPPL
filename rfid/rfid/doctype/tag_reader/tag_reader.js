// Copyright (c) 2023, soham.pawar@erpdata.in and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tag Reader', {
	onload(frm) {
            frm.call({
				method:'get_rfid_info',
				doc:frm.doc,
				
			}) 
	 },
	});
frappe.ui.form.on('Tag Reader', {
	start_reading:function(frm) {
		frm.call({
			method:'get_rfid',
			doc:frm.doc,
			
		}) 
 },
});
// frappe.ui.form.on('Tag Reader', {
// 	before_save:function(frm) {
// 		frm.call({
// 			method:'assign_tag_value',
// 			doc:frm.doc,
// 		}) 
//  },});

 frappe.ui.form.on('Tag Reader', {
	transportar:function(frm) {
	frm.call({
		method:'validate_transporter',
		doc:frm.doc,
		
	}) 
},
});
// frappe.ui.form.on('Tag Reader', {
// 	token_number:function(frm) {
// 	   frm.call({
// 		   method:'validate_token_number',
// 		   doc:frm.doc,
		   
// 	   }) 
// },
// });

