# Automated Production Deployment (GitHub Actions + AWS SSM)

`/.github/workflows/deploy-production.yml` deploys `main` to the production EC2 host automatically on every push (and can also be run manually from the Actions tab). It reuses the exact "Routine deployment update" steps from `docs/guides/DEPLOYMENT.md` (§10) — backup the DB, `git pull`, rebuild, `up -d`, health check — but runs them remotely via AWS Systems Manager (SSM) Run Command instead of an interactive SSH session. No SSH port needs to be open and no long-lived AWS keys are stored in GitHub.

## Why SSM instead of SSH

- No inbound port 22 required — traffic goes through the SSM agent, not a directly reachable SSH port.
- No private key material stored as a GitHub secret.
- All command output is logged in the AWS console (CloudTrail + SSM run history) for audit.

## One-time AWS setup

1. **Attach an IAM instance profile to the EC2 host** with the AWS-managed policy `AmazonSSMManagedInstanceCore`. Confirm the SSM agent is running (`sudo systemctl status amazon-ssm-agent` — pre-installed on Ubuntu 22.04/24.04 AMIs; the instance also needs outbound HTTPS to reach the SSM endpoints).
2. **Confirm the instance is registered**: AWS Console → Systems Manager → Fleet Manager, or:
   ```bash
   aws ssm describe-instance-information --query "InstanceInformationList[].InstanceId"
   ```
3. **Create an IAM OIDC identity provider for GitHub Actions** (skip if your AWS account already has one): provider URL `https://token.actions.githubusercontent.com`, audience `sts.amazonaws.com`.
4. **Create an IAM role** (e.g. `github-actions-deploy-gokservices`) with a trust policy scoped to this repo's `production` Environment. Because the deploy job declares `environment: production`, GitHub issues an OIDC token whose `sub` claim is `repo:<owner>/<repo>:environment:production` (not the `ref:refs/heads/...` form used by non-environment jobs) — the trust policy must match that exact form:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Effect": "Allow",
       "Principal": { "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com" },
       "Action": "sts:AssumeRoleWithWebIdentity",
       "Condition": {
         "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" },
         "StringLike": { "token.actions.githubusercontent.com:sub": "repo:BITZ-IT-Consulting-LTD/ictapoc:environment:production" }
       }
     }]
   }
   ```
5. **Attach a minimal permissions policy** to that role — only what `ssm send-command`/`get-command-invocation`/`wait command-executed` need:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Effect": "Allow",
       "Action": ["ssm:SendCommand", "ssm:GetCommandInvocation", "ssm:ListCommandInvocations"],
       "Resource": [
         "arn:aws:ec2:<REGION>:<ACCOUNT_ID>:instance/<EC2_INSTANCE_ID>",
         "arn:aws:ssm:<REGION>::document/AWS-RunShellScript"
       ]
     }]
   }
   ```

## GitHub repository configuration

Create a `production` [Environment](https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment) (Settings → Environments) — this lets you require manual approval before deploys run, and scopes the secrets below to it.

**Secrets** (Settings → Environments → `production` → Secrets):

| Name | Value |
|---|---|
| `AWS_DEPLOY_ROLE_ARN` | ARN of the IAM role created above |
| `EC2_INSTANCE_ID` | The production instance's `i-xxxxxxxx` ID |

**Variables** (same screen, Variables tab):

| Name | Value |
|---|---|
| `AWS_REGION` | e.g. `eu-west-1` |

## What the workflow does

1. Assumes the AWS IAM role via OIDC (no static keys).
2. Sends an `AWS-RunShellScript` SSM command to the instance that, on the host:
   - `pg_dump`s the database to `backups/` before touching anything
   - `git fetch` + hard-resets `/opt/gokservices/app` to `origin/main`
   - `docker compose -f docker-compose.prod.yml build --pull && up -d --remove-orphans`
   - polls `https://gokservices.bitz-itc.com/ready` until it succeeds (or fails the job after ~1 minute)
3. Waits for the SSM command to finish and fails the GitHub Actions run (with logs) if the remote script exited non-zero.

## Notes / things to decide before enabling

- The workflow uses `git reset --hard origin/main` on the host, which discards any uncommitted local changes in `/opt/gokservices/app` — that directory should only ever be updated by this workflow, not edited by hand.
- Add a required reviewer on the `production` Environment if you want a manual approval gate before deploys actually run (recommended, since this pushes to a public POC referenced in `docs/guides/DEPLOYMENT.md`).
- This does **not** run database migrations separately — they run automatically inside the backend container's entrypoint on start, same as manual deploys.
- Rollback is still manual: SSH/SSM in and follow `docs/guides/DEPLOYMENT.md` §12, or re-run this workflow after reverting `main`.
