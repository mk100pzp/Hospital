import pro1_operator
enter=[{
"name":"main",
"children":[{
        "name":"registration",
        "children":[
                        {
                            "name":"doctor",
                            "action":[pro1_operator.doctor_registration],
                            

                        },
                        {
                            "name":"patient",
                            "action":[pro1_operator.patient_registeration],
                            
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
                                        "function":[pro1_operator.login_doctor],
                                        "action":[pro1_operator.add_visit_time]
                                        },



                                    
                                        {
                                        "name":"edit visit time",
                                        "function":[pro1_operator.login_doctor],
                                        "action":[pro1_operator.edit_visit_time]
                                        },
                                        {
                                        "name":"remove visit time",
                                        "function":[pro1_operator.login_doctor],
                                        "action":[pro1_operator.remove_visit_time]
                                        },

                            ]

                        },
                        {
                            "name":"patient",
                            
                            "children":[{
                                    "function":[pro1_operator.login_patient],
                                    "name":"get visit time",
                                    "action":[pro1_operator.get_visit_time,pro1_operator.create_medical_record]
                                    },



                                
                                    {"function":[pro1_operator.login_patient],
                                    "name":"cancel visit time",
                                    "action":[pro1_operator.cancel_visit_time]
                                    },
                                
                                    {"function":[pro1_operator.login_patient],
                                    "name":"show catched visit time",
                                    "action":[pro1_operator.catched_visit_time]
                                    },

                                    {"function":[pro1_operator.login_patient],
                                    "name":"show bill",
                                    "action":[pro1_operator.show_bill]
                                    },

                                    {"function":[pro1_operator.login_patient],
                                    "name":"show visit form",
                                    "action":[pro1_operator.show_visit_form]
                                    },

                            ]

                        },
                        {
                            "name":"admin",
                            "children":[
                                {
                                        "function":[pro1_operator.login_admin],
                                        "name":"add new admin",
                                    "action":[pro1_operator.add_new_admin]
                                    },



                                
                                    {
                                        "function":[pro1_operator.login_admin],
                                        "name":"show patient information",
                                    "action":[pro1_operator.show_patient_information]
                                    },

                                    {
                                        "function":[pro1_operator.login_admin],
                                        "name":"show doctor information",
                                    "action":[pro1_operator.show_doctor_information]
                                    },

                                    {  "function":[pro1_operator.login_admin],
                                        "name":"income of visit",
                                    "action":[pro1_operator.income_visit]
                                    },

                                    {
                                        "function":[pro1_operator.login_admin],
                                        "name":"show number of patient's visits",
                                    "action":[pro1_operator.number_visits]
                                    },

                                    {   "function":[pro1_operator.login_admin],
                                        "name":"income of hospital",
                                    "action":[pro1_operator.income_hospital]
                                    },
                                    {   "function":[pro1_operator.login_admin],
                                        "name":"show log ",
                                    "action":[pro1_operator.show_log]
                                    }

                                                            ]
                                                        
                                                        }
                                        ]
                                                        
                                    }

]}
]


