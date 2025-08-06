## Issue: Tar Error in Deploy-Ready Job

### Description
There is an error occurring in the deploy-ready job related to the `tar` command. This issue causes deployment failures that can impact our release process.

### Suggested Solution
To prevent these deployment failures, it is recommended to use the `--ignore-failed-read` option with the `tar` command. This option allows the tar operation to continue even if it encounters errors while reading files.

### Action Items
- Review the current usage of the `tar` command in the deploy-ready job.
- Update the command to include the `--ignore-failed-read` option where appropriate.