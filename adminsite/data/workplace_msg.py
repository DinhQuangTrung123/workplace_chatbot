class WorkplaceMessage(object):
    msg_workplace_basic = {
        "recipient": {},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "This is test text",
                    "buttons": [{
                                "type": "postback",
                                "title": "Đồng Ý",
                                "payload": "input content you need show"
                        },
                                {
                                "type": "postback",
                                "title": "Từ Chối",
                                "payload": "input content you need show"
                        }
                    ]
                }
            }
        }
    }
    msg_workplace_to_users_id = {
        "recipient": {
            "ids": []
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "This is test text",
                    "buttons": [{
                        "type": "postback",
                        "title": "Đồng Ý",
                        "payload": "input content you need show"
                    },
                        {
                            "type": "postback",
                            "title": "Từ Chối",
                            "payload": "input content you need show"
                        }
                    ]
                }
            }
        }
    }

    msg_workplace_to_user_id = {
        # new thread to user id

    }

    button_web_url = {
        "type": "web_url",
        "url": "input your url",
        "title": "input content you need show"
    }

    button_postback = {
        "type": "postback",
        "title": "input your title",
        "payload": "input content you need show"
    }

    button_call_phonenumber = {
        "type": "phone_number",
        "title": "Call Phone Number",
        "payload": "input phoneumber you need call"
    }