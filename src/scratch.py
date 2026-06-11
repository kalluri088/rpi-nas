from auth import create_access_token

token = create_access_token(
	{"sub" : "admin"}
)

print(token)
