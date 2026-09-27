# PROJ-104: Export to CSV times out for boards over 5,000 issues
Status: In Progress | Type: Bug | Fix version: 2.4.1
Large boards hit the 30 second API gateway timeout during CSV export. Proposed fix:
move export to a background job, write the file to S3, and email the user a signed
download link when it finishes. Needs a new jobs table and a worker process.
