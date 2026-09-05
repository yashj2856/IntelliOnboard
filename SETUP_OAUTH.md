# Setting up real Google APIs (personal OAuth2, free)

This lets the agent create **real** Drive folders, Calendar events, Gmail
emails, and Sheets under your own Google account — no Google Workspace
domain required. Everything below is free.

You only need to do this once. Skip it entirely if you're happy running in
Simulation Mode.

---

## 1. Create a Google Cloud project

1. Go to https://console.cloud.google.com/
2. Top left, click the project dropdown → **New Project**
3. Name it e.g. `onboarding-agent` → **Create**
4. Make sure the new project is selected in the top dropdown.

## 2. Enable the 4 APIs

Go to **APIs & Services > Library** and enable each of these (search the
name, click it, click **Enable**):

- Google Drive API
- Google Calendar API
- Gmail API
- Google Sheets API

## 3. Configure the OAuth consent screen

1. **APIs & Services > OAuth consent screen**
2. User type: **External** → Create
3. App name: anything (e.g. "Onboarding Agent Demo"), pick your email for
   support email and developer contact → Save and Continue
4. Scopes step: click **Save and Continue** (you don't need to add scopes
   here — the app requests them directly)
5. Test users step: click **Add Users** → add your own Gmail address →
   Save and Continue
6. Leave the app in **Testing** publishing status. (This is fine —
   "Testing" apps work indefinitely for accounts listed as test users; you
   don't need Google's app verification for a personal/portfolio project.)

## 4. Create an OAuth Client ID

1. **APIs & Services > Credentials**
2. **Create Credentials > OAuth client ID**
3. Application type: **Desktop app**
4. Name: anything (e.g. "onboarding-agent-desktop") → Create
5. Click **Download JSON** on the client you just created

## 5. Place the credentials file

In your cloned repo folder:

```bash
mkdir -p credentials
mv ~/Downloads/client_secret_XXXXX.json credentials/oauth_client.json
```

(`credentials/` is already in `.gitignore` — this file will never be
committed.)

## 6. Run the one-time authorization (on your HOST machine, not Docker)

You need Python + the two auth packages locally for this one step:

```bash
pip install google-auth-oauthlib google-auth
python3 authorize_google.py
```

A browser window opens → sign in with the **same Google account** you
added as a test user in step 3 → click through the "Google hasn't verified
this app" warning (Advanced > Go to onboarding-agent-demo — this warning is
normal and expected for apps in Testing mode) → approve the requested
permissions.

You'll see:
```
✅ Authorized. Token saved to 'credentials/token.json'.
```

## 7. Run the app for real

```bash
docker compose up --build
```

Open http://localhost:8501, and in the sidebar **turn OFF Simulation
Mode**. Onboarding requests now create real folders in your Drive, real
events on your Calendar, and send real emails from your Gmail.

---

### Notes

- The OAuth token refreshes itself automatically — you shouldn't need to
  re-run `authorize_google.py` unless you delete `credentials/token.json`
  or revoke access.
- To revoke access at any time: https://myaccount.google.com/permissions
- Since the app is in "Testing" mode, only the test users you listed in
  step 3 can authorize it — that's expected and fine for a personal demo.
- Emails will be sent **from your own Gmail address**. For a demo, either
  onboard a fictional person and send to your own inbox, or use a second
  free Gmail account as the "new hire" so you can see the emails land.
