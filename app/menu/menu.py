from app.authentication import auth
from app.database import db
from app.models import models

enter = [{
    "name": "main",
    "children": [{
        "name": "registration",
        "children": [
            {
                "name": "doctor",
                "action": [auth.Authentication.doctor_registration],

            },
            {
                "name": "patient",
                "action": [auth.Authentication.patient_registeration],

            },

        ]
    },

        {
            "name": "log in",
            "children": [
                {
                    "name": "doctor",

                    "children": [{
                        "name": "add visit time",
                        "function": [auth.Authentication.login_doctor],
                        "action": [models.Visit_Date.create_visit_date]
                    },

                        {
                            "name": "remove visit time",
                            "function": [auth.Authentication.login_doctor],
                            "action": [models.Visit_Date.remove_visit_time]
                        },

                    ]

                },
                {
                    "name": "patient",

                    "children": [{
                        "function": [auth.Authentication.login_patient],
                        "name": "get visit time",
                        "action": [models.Paient.get_visit_time]
                    },

                        {"function": [auth.Authentication.login_patient],
                         "name": "cancel visit time",
                         "action": [models.Paient.cancel_visit_time]
                         },

                        {"function": [auth.Authentication.login_patient],
                         "name": "show catched visit time",
                         "action": [models.Paient.show_visit_time]
                         },

                        {"function": [auth.Authentication.login_patient],
                         "name": "show bill",
                         "action": [models.Paient_Bill.show_bill]
                         },

                        {"function": [auth.Authentication.login_patient],
                         "name": "show visit form",
                         "action": [models.Paient.show_visit_form]
                         },

                    ]

                },
                {
                    "name": "admin",
                    "children": [
                        {
                            "function": [auth.Authentication.login_admin],
                            "name": "add new admin",
                            "action": [models.Admin.add_new_admin]
                        },

                        {
                            "function": [auth.Authentication.login_admin],
                            "name": "show patient information",
                            "action": [models.Paient.search_patient_information]
                        },

                        {
                            "function": [auth.Authentication.login_admin],
                            "name": "show doctor information",
                            "action": [models.Doctor.search_doctor_information]
                        },

                        {"function": [auth.Authentication.login_admin],
                         "name": "income of visit",
                         "action": [models.Doctor.search_income_visit]
                         },

                        {
                            "function": [auth.Authentication.login_admin],
                            "name": "show number of patient's visits",
                            "action": [models.Visit_Form.show_number_visit]
                        },

                        {"function": [auth.Authentication.login_admin],
                         "name": "income of hospital",
                         "action": [models.Paient_Bill.show_income_hospital]
                         },
                        {"function": [auth.Authentication.login_admin],
                         "name": "show log info ",
                         "action": [models.show_log_info]
                         },
                        {"function": [auth.Authentication.login_admin],
                         "name": "show log error",
                         "action": [models.show_log_error]
                         }

                    ]

                }
            ]

        }

    ]}
]
