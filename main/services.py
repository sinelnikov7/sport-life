import jwt
from sport_life.settings import SECRET_KEY
#
#
def get_user_id(request):
    token = request.headers.get('Authorization').split(' ')[1]
    user_id = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])['user_id']
    return user_id

