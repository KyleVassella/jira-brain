# PROJ-108: Attachment upload fails for files over 25 MB
Status: Done | Type: Bug | Fix version: 2.4.0
Uploads larger than 25 MB returned a 413 error. Root cause: nginx client_max_body_size
was set to 25m while the app limit was 100 MB. Fix: raised the nginx limit to 100m and
added a client-side size check with a clear error message before the upload starts.
