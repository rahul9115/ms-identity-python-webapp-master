import re

reg=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
email="das"
print(re.fullmatch(reg,email))