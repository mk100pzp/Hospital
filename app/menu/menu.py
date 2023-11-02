from app.authentication import auth
from app.database import db
from app.models import models

enter=[{
"name":"main",
"children":[{
        "name":"registration",
        "children":[
                        {
                            "name":"doctor",
                            "action":[auth.Authentication.doctor_registration],
                            

                        },
                        {
                            "name":"patient",
                            "action":[auth.Authentication.patient_registeration],
                            
                        },
                        
                    ]
    },



  
    {
        "name":"log in",
        "children":[
                        {
                            "name":"doctor",
                           
                           "children":[{
                                        "name":"add visit time",
                                        "function":[auth.Authentication.login_doctor],
                                        "action":[db.Database.add_visit_time]
                                        },



                                    
                                        {
                                        "name":"edit visit time",
                                        "function":[auth.Authentication.login_doctor],
                                        "action":[db.Database.edit_visit_time]
                                        },
                                        {
                                        "name":"remove visit time",
                                        "function":[auth.Authentication.login_doctor],
                                        "action":[db.Database.remove_visit_time]
                                        },

                            ]

                        },
                        {
                            "name":"patient",
                            
                            "children":[{
                                    "function":[auth.Authentication.login_patient],
                                    "name":"get visit time",
                                    "action":[models.Visit_Date.get_visit_time, models.Medical_Record.create_medical_record]
                                    },



                                
                                    {"function":[auth.Authentication.login_patient],
                                    "name":"cancel visit time",
                                    "action":[models.Visit_Date.cancel_visit_time]
                                    },
                                
                                    {"function":[auth.Authentication.login_patient],
                                    "name":"show catched visit time",
                                    "action":[db.Database.catched_visit_time]
                                    },

                                    {"function":[auth.Authentication.login_patient],
                                    "name":"show bill",
                                    "action":[db.Database.show_bill]
                                    },

                                    {"function":[auth.Authentication.login_patient],
                                    "name":"show visit form",
                                    "action":[db.Database.show_visit_form]
                                    },

                            ]

                        },
                        {
                            "name":"admin",
                            "children":[
                                {
                                        "function":[auth.Authentication.login_admin],
                                        "name":"add new admin",
                                    "action":[models.Admin.add_new_admin]
                                    },



                                
                                    {
                                        "function":[auth.Authentication.login_admin],
                                        "name":"show patient information",
                                    "action":[db.Database.show_patient_information]
                                    },

                                    {
                                        "function":[auth.Authentication.login_admin],
                                        "name":"show doctor information",
                                    "action":[db.Database.show_doctor_information]
                                    },

                                    {  "function":[auth.Authentication.login_admin],
                                        "name":"income of visit",
                                    "action":[db.Database.show_income_visit]
                                    },

                                    {
                                        "function":[auth.Authentication.login_admin],
                                        "name":"show number of patient's visits",
                                    "action":[db.Database.show_number_visits]
                                    },

                                    {   "function":[auth.Authentication.login_admin],
                                        "name":"income of hospital",
                                    "action":[db.Database.show_income_hospital]
                                    },
                                    {   "function":[auth.Authentication.login_admin],
                                        "name":"show log ",
                                    "action":[db.Database.show_log_info]
                                    },
                                    {   "function":[auth.Authentication.login_admin],
                                        "name":"show log ",
                                    "action":[db.Database.show_log_error]
                                    }

                                                            ]
                                                        
                                                        }
                                        ]
                                                        
                                    }

]}
]

