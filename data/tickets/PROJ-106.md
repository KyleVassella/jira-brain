# PROJ-106: Search returns stale results after issue is edited
Status: Done | Type: Bug | Fix version: 2.4.0
Editing an issue summary did not update search results for up to 10 minutes.
Root cause: the search index was only rebuilt by a scheduled job. Fix: publish an
index-update event on every issue save so the indexer updates that document immediately.
