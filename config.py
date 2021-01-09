import string
import os

token = '1535946117:AAE_XgVH6phVFCE9TagZqkWR54-o6UoUHso'
port = int(os.environ.get('PORT', '5000'))
app_name = 'the-library-of-babel-bot'

lines_count = 25
line_len = 50
library = {
    'page_len': lines_count * line_len,
    'mult': pow(30, lines_count * line_len),
    'title_len': 30,
    'digs': string.digits + string.ascii_lowercase,
    'alphabet': string.ascii_lowercase+', .',
    'wall': 4,
    'shelf': 4,
    'volume': 15,
    'page': 410
}
