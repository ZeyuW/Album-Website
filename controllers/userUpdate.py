import re, uuid, hashlib

def exists(a):
    return 'This username is taken' if a else None

def length_comp(prefix, cur_str, length, large):
    #should >= length
    if large:  
        return prefix + ' must be at least '+ str(length) + ' characters long' if len(cur_str)<length else None
    #should <= length
    else:      
        return prefix + ' must be no longer than 40 characters' if len(cur_str)>length else None

def allowed(prefix, cur_str):
    return prefix + ' may only contain letters, digits, and underscores' if not re.match("^[0-9A-Za-z_]*$", cur_str) else None

def atleast(cur_str):
    return 'Passwords must contain at least one letter and one number' if not re.match("^(?=.*[a-zA-Z])(?=.*\d).+$", cur_str) else None

def email_context(cur_str):
    return 'Email address must be valid' if not re.match(r"[^@]+@[^@]+\.[^@]+", cur_str) else None



def password_hash(password1):
    algorithm='sha512'
    salt=uuid.uuid4().hex
    m = hashlib.new(algorithm)
    m.update(salt + password1)
    return(algorithm + '$' + salt + '$' + m.hexdigest())


def check_username(cur_str, a):
    result = [  exists(a),
                length_comp('Usernames', cur_str, 3, True),
                allowed('Usernames', cur_str),
                length_comp('username', cur_str, 20, False)
             ]
    return [item for item in result if item]

def check_firstname(cur_str):
    result = [ length_comp('Firstname', cur_str, 20, False) ]
    return [item for item in result if item]

def check_lastname(cur_str):
    result = [ length_comp('Lastname', cur_str, 20, False) ]
    return [item for item in result if item]

def check_email(cur_str):
    result = [ email_context(cur_str),
               length_comp('Email', cur_str, 40, False) ]
    return [item for item in result if item]

def check_password1(cur_str):
    result = [ length_comp('Passwords', cur_str, 8, True),
               allowed('Passwords', cur_str),
               atleast(cur_str) ]
    return [item for item in result if item]

def check_password2(cur_str, another):
    result = ['Passwords do not match' if cur_str!=another else None ]
    return [item for item in result if item]
    
    

    





    

