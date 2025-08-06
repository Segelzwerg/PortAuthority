## Issue: Tar Error in Deploy-Ready Job

### Description
During the deploy-ready job, an error occurs when creating the deployment artifact. The following errors are encountered:

```
tar: .: file changed as we read it
Process completed with exit code 1.
```

### Steps to Reproduce
1. Trigger the deploy-ready job in the CI/CD pipeline.
2. Monitor the job logs during the artifact creation step.

### Expected Behavior
The deployment artifact should be created successfully without errors, allowing the deployment to proceed.

### Actual Behavior
The job fails with the tar error, preventing the deployment from completing.

### Suggested Fix
To prevent this error from occurring, it's recommended to update the tar command to include the `--ignore-failed-read` option. This option will allow the tar command to ignore files that change while being read, thus preventing deployment failures due to this issue.