import uuid

print(type(str(uuid.uuid4())))
id = ''.join(str(uuid.uuid4()).split("-"))[:16]
print(id)