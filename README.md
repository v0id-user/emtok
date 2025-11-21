# Email Tokenization Demo

This project is a quick demonstration of a security practice: tokenizing emails when storing user identities.

## How it works (see `main.py`):

- When a new identity is created, the email is tokenized using a hash function (`hash_email_token`).
- The actual email and its token are stored in a separate `EmailTokens` table.
- The `Identities` table references the token, not the email address directly.
- This approach adds a layer of abstraction and security, so emails are not stored with user credentials.

> **Note:** The hashing/tokenization used here is for demonstration purposes, not for production!

## Try it

```
uv venv
uv pip isntall peewee
uv run main.py
```

You’ll see output of tokens and identities generated for demo users in the console.

