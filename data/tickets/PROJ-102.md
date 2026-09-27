# PROJ-102: Dashboard charts render blank on first load
Status: Done | Type: Bug | Fix version: 2.3.1
The sprint velocity chart shows an empty canvas until the user resizes the window.
Root cause: chart library initialized before the container had a measured width.
Fix: defer chart init until after the layout pass using a ResizeObserver.
