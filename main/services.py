# import jwt
# from sport_life.settings import SECRET_KEY
#
#
# def validate_token_and_user(request, pk):
#     token = request.headers.get('Authorization').split(' ')[1]
#     user_id = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])['user_id']
#     if