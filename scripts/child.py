class Child(object):
    def __init__(self, child_id, child_name, parent_id, parent_name, email, cc_email, send_email):
        # Meta data details
        self.child_id = child_id
        self.child_name = child_name
        self.parent_id = parent_id
        self.parent_name = parent_name
        self.email = email
        self.cc_email = cc_email
        self.send_email = send_email

