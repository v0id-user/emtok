from peewee import CharField, DateTimeField, ForeignKeyField, Model, SqliteDatabase
import hashlib
from datetime import datetime
import secrets

db = SqliteDatabase('emtok.db')

def generate_id():
    return secrets.token_hex(16)

def hash_password(password: str) -> str:
    salt = b'static_salt'
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
    return dk.hex()

def hash_email_token(email: str) -> str:
    return hashlib.sha256(email.encode()).hexdigest()[:16] # This is not safe for production, but it's fine for this example


class BaseModel(Model):
    class Meta:
        database = db


class EmailTokens(BaseModel):
    token = CharField(primary_key=True, max_length=32)
    email = CharField(unique=True)
    created_at = DateTimeField(default=datetime.now)


class Identities(BaseModel):
    id = CharField(primary_key=True, default=generate_id, max_length=32)
    username = CharField()
    password = CharField()
    email_token = ForeignKeyField(EmailTokens, backref='identities', to_field='token')
    created_at = DateTimeField(default=datetime.utcnow)


def init_db():
    db.connect()
    db.create_tables([EmailTokens, Identities])


def create_email_token(email: str) -> EmailTokens:
    token = hash_email_token(email)
    email_obj, _ = EmailTokens.get_or_create(
        token=token,
        defaults={
            "email": email
        }
    )
    return email_obj


def create_identity(username: str, password: str, email: str):
    email_token_record = create_email_token(email)
    Identities.create(
        username=username,
        password=hash_password(password),
        email_token=email_token_record
    )


def leak_table_data():
    print("\nEmail Tokens:")
    for e in EmailTokens.select():
        print(e.token, e.email, e.created_at)

    print("\nIdentities:")
    for i in Identities.select():
        print(i.id, i.username, i.email_token.token, i.created_at)


def random_word():
    import random
    verbs = ['run', 'jump', 'fly', 'read', 'write', 'sing']
    nouns = ['tree', 'cat', 'car', 'apple', 'river', 'cloud']
    return f"{random.choice(verbs)}_{random.choice(nouns)}"


def main():
    init_db()

    for _ in range(3):
        u = random_word()
        p = random_word()
        e = f"{random_word()}@example.com"
        create_identity(u, p, e)

    leak_table_data()


if __name__ == "__main__":
    main()
