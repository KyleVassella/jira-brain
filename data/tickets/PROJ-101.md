# PROJ-101: Login fails with SSO on Safari
Status: Done | Type: Bug | Fix version: 2.3.1
Users on Safari 17 get a blank page after SSO redirect. Root cause: SameSite cookie
default changed. Fix: set SameSite=None; Secure on the session cookie.