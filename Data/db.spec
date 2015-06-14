users:STRING name, STRING password, STRING email
roles:STRING name
groups:STRING name
user_roles:FOREIGN_KEY users, FOREIGN_KEY roles
accounts:STRING code, STRING name, FOREIGN_KEY accounts parent 0, FOREIGN_KEY groups
transactions:FOREIGN_KEY accounts from, FOREIGN_KEY accounts to
reports:STRING name, FOREIGN_KEY groups
