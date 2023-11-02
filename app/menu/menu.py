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
                            "action":[auth.doctor_registration],
                            

                        },
                        {
                            "name":"patient",
                            "action":[auth.patient_registeration],
                            
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
                                        "function":[auth.login_doctor],
                                        "action":[db.add_visit_time]
                                        },



                                    
                                        {
                                        "name":"edit visit time",
                                        "function":[auth.login_doctor],
                                        "action":[db.edit_visit_time]
                                        },
                                        {
                                        "name":"remove visit time",
                                        "function":[auth.login_doctor],
                                        "action":[db.remove_visit_time]
                                        },

                            ]

                        },
                        {
                            "name":"patient",
                            
                            "children":[{
                                    "function":[auth.login_patient],
                                    "name":"get visit time",
                                    "action":[models.get_visit_time, models.create_medical_record]
                                    },



                                
                                    {"function":[auth.login_patient],
                                    "name":"cancel visit time",
                                    "action":[models.cancel_visit_time]
                                    },
                                
                                    {"function":[auth.login_patient],
                                    "name":"show catched visit time",
                                    "action":[db.catched_visit_time]
                                    },

                                    {"function":[auth.login_patient],
                                    "name":"show bill",
                                    "action":[db.show_bill]
                                    },

                                    {"function":[auth.login_patient],
                                    "name":"show visit form",
                                    "action":[db.show_visit_form]
                                    },

                            ]

                        },
                        {
                            "name":"admin",
                            "children":[
                                {
                                        "function":[auth.login_admin],
                                        "name":"add new admin",
                                    "action":[models.add_new_admin]
                                    },



                                
                                    {
                                        "function":[auth.login_admin],
                                        "name":"show patient information",
                                    "action":[db.show_patient_information]
                                    },

                                    {
                                        "function":[auth.login_admin],
                                        "name":"show doctor information",
                                    "action":[db.show_doctor_information]
                                    },

                                    {  "function":[auth.login_admin],
                                        "name":"income of visit",
                                    "action":[db.show_income_visit]
                                    },

                                    {
                                        "function":[auth.login_admin],
                                        "name":"show number of patient's visits",
                                    "action":[db.show_number_visits]
                                    },

                                    {   "function":[auth.login_admin],
                                        "name":"income of hospital",
                                    "action":[db.show_income_hospital]
                                    },
                                    {   "function":[auth.login_admin],
                                        "name":"show log ",
                                    "action":[db.show_log_info]
                                    },
                                    {   "function":[auth.login_admin],
                                        "name":"show log ",
                                    "action":[db.show_log_error]
                                    }

                                                            ]
                                                        
                                                        }
                                        ]
                                                        
                                    }

]}
]

