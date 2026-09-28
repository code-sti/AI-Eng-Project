# Contact Book (CRUD, JSON Storage)

A command-line contact book in Python with full CRUD (Create, Read, Update, Delete) and name search, storing data persistently in a JSON file.

**Part of my 200+ project [Zero-to-Senior AI Engineer + Solutions Architect](#) learning path — Project F.3.**

## 📘 Learn this project step by step

**→ [Learning.md](./Learning.md)** — the full teaching guide: every step explained, all topics covered, and the soft skills this project builds. Start there if you want to learn by rebuilding this yourself.

## What it does

- Add a contact (name, phone, email)
- View all contacts
- Search contacts by partial name match
- Update a contact (change only the fields you want, leave others blank to keep them)
- Delete a contact
- Everything saved automatically to `contacts.json`

## Run it

```bash
python contact_book.py
```

Requires Python 3.6+. No external dependencies (uses only `json` and `os` from the standard library).

## Example

```
--- Contact Book ---
1. View contacts
2. Add contact
3. Search contact
4. Update contact
5. Delete contact
6. Exit
Choose an option: 2
Name: John Smith
Phone: 555-1234
Email: john@example.com
Added contact: John Smith
```

## Suggested extra-skill upgrade

Once comfortable with this version, try rebuilding contact validation using **Pydantic** instead of plain dictionaries — this is the same tool used later for FastAPI and AI agent structured outputs. See `Learning.md` for details.