with open("client.py", "r") as f:
    content = f.read()

# Fix the quote issues
content = content.replace("''utf-8''", '"utf-8"')
content = content.replace("''{'", '"{')
content = content.replace("''}'", '"}"')
content = content.replace("''reason''", '"reason"')

with open("client.py", "w") as f:
    f.write(content)

print("Fixed client.py!")
