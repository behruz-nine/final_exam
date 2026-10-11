import re
from rest_framework.exceptions import ValidationError

input_email = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
input_phone = re.compile(r'/^[+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/gmi')

def input_regix(user_input):
    if re.fullmatch(input_email, user_input):
        return 'via_email'
    
    elif re.fullmatch(input_phone, user_input):
        return 'via_phone'
    
    else:
        raise ValidationError('Email yoki phone_number xato kiritildi qayta kiriting!')
