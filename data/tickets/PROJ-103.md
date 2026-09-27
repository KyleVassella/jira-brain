# PROJ-103: Add dark mode toggle to user settings
Status: Done | Type: Feature | Fix version: 2.4.0
Users requested a dark theme. Added a toggle under Settings > Appearance that persists
to the user profile. Theme is applied via a data-theme attribute on the root element
and CSS custom properties. Default follows the OS prefers-color-scheme setting.
