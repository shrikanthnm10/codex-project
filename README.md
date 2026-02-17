# Python ERP CI/CD Project (GitHub + AWS CloudFormation + CodePipeline)

## Quick Checklist (What you will do)
- Design one reproducible AWS architecture using CloudFormation.
- Keep ERP source code in GitHub and trigger deployments from commits.
- Build and test Python ERP app automatically with CodeBuild.
- Deploy to EC2 Auto Scaling instances using CodeDeploy.
- Use RDS MySQL as ERP database and externalize configuration.
- Measure stack create/delete timings and document results.

---

## 1) Project Overview
This project demonstrates a **professional beginner-friendly CI/CD setup**:
- **Source:** GitHub
- **Infra as Code:** AWS CloudFormation
- **CI:** AWS CodeBuild
- **CD:** AWS CodeDeploy + AWS CodePipeline
- **Application:** Python Flask ERP starter app
- **Database:** Amazon RDS MySQL

When the CloudFormation stack is deleted and created again, all services are relaunched with the same template configuration.

---

## 2) Repository Structure

```text
.
├── app/                     # ERP Python application package
├── templates/               # HTML template (dashboard)
├── tests/                   # Unit tests
├── cloudformation/
│   └── erp-cicd.yaml        # Full infrastructure template
├── codedeploy/              # Deployment lifecycle scripts
├── scripts/
│   ├── init_db.py
│   └── track_stack_times.sh
├── buildspec.yml            # CodeBuild instructions
├── appspec.yml              # CodeDeploy instructions
├── requirements.txt
└── .env.example
```

---

## 3) How AWS Services Work + Why Used (English + Tamil)

| Service | Why this service? (English) | Use case (Tamil - simple) |
|---|---|---|
| GitHub | Stores source code, version history, branch collaboration. | **Code store panna** use pannuvom; team la work panna easy.
| CloudFormation | Creates all AWS resources from one template; reproducible infra. | **One template la** ellaa AWS resources create aagum; repeat panna same output.
| CodePipeline | Orchestrates end-to-end flow (Source → Build → Deploy). | Commit pannina udane automatic stages run ஆகும்.
| CodeBuild | Installs deps, runs tests, prepares deploy artifact. | App build + test automatic ah nadakkum.
| CodeDeploy | Deploys artifact safely to EC2/ASG instances. | Server ku new code copy panni service restart pannum.
| EC2 Auto Scaling | Hosts app with self-healing instances. | Instance down ஆனாலும் pudhusa spawn ஆகும்.
| RDS MySQL | Managed relational DB for ERP tables (customers/orders). | ERP-ku structured data store pannuradhu idhu.
| IAM Roles | Secure permission boundaries between services. | Service-kku thevaiyana access mattum kudukkum.
| S3 Artifact Bucket | Stores pipeline build/deploy artifacts. | Build output temporary store pannum.

---

## 4) Step-by-Step Implementation Guide (English)

### Step 1: Create GitHub Repository
1. Create a new repo (example: `erp-cicd-project`).
2. Push this code.
3. Keep default branch as `main`.

**Validation:** GitHub repo opens and all project files are visible.

### Step 2: Create CodeStar Connection to GitHub
1. AWS Console → Developer Tools → CodePipeline → Connections.
2. Create connection and authorize GitHub account/repo.
3. Copy the **Connection ARN**.

**Validation:** Connection status should be `Available`.

### Step 3: Deploy CloudFormation Stack
1. Open CloudFormation → Create stack → Upload `cloudformation/erp-cicd.yaml`.
2. Enter parameters:
   - GitHub owner/repo/branch
   - CodeStar connection ARN
   - VPC + subnets
   - DB username/password
3. Check IAM capability and create stack.

**Validation:** Stack status should become `CREATE_COMPLETE`.

### Step 4: Verify Pipeline Auto Trigger
1. Open CodePipeline from stack outputs.
2. Ensure source, build, deploy stages pass.

**Validation:** Pipeline execution is `Succeeded`.

### Step 5: Verify ERP App + DB
1. Find EC2 instance in ASG.
2. Open instance public IP on port 8000 (or via load balancer if added).
3. Call `/health` and `/`.

**Validation:** `/health` returns `{"status":"ok"}` and dashboard loads.

### Step 6: Track Create/Delete Time
Run:
```bash
./scripts/track_stack_times.sh <stack-name> cloudformation/erp-cicd.yaml
```
Update `docs/stack-time-log.md` with observed times.

**Validation:** Script prints both create and delete time in seconds.

### Step 7: Reproducibility Check
1. Delete stack.
2. Re-create stack with same parameters.
3. Trigger pipeline and verify deployment.

**Validation:** Same services are recreated and pipeline succeeds again.

---

## 5) Beginner-Friendly Tamil Guide (Konjam Brief + Clear)

### Step-by-step (Tamil)
1. **GitHub repo create பண்ணு**, இந்த project files push பண்ணு.
2. AWS la **CodeStar Connection** create பண்ணி GitHub connect பண்ணு.
3. **CloudFormation template upload** பண்ணி stack create பண்ணு.
4. Stack create ஆனதும் **CodePipeline automatic run** ஆகும்.
5. Build stage la test pass ஆகணும்; Deploy stage la app EC2க்கு போகும்.
6. EC2 IP + `:8000/health` open பண்ணி app check பண்ணு.
7. `track_stack_times.sh` run பண்ணி create/delete நேரம் note பண்ணு.
8. Stack delete பண்ணிட்டு மீண்டும் create பண்ணு → same services வந்தா success.

### Common Errors + Quick Fix
- **GitHub source fail:** Connection ARN wrong / branch name mismatch → parameter correct பண்ணு.
- **Build fail:** requirements install issue → `requirements.txt` verify பண்ணு.
- **Deploy fail:** CodeDeploy agent running இல்ல → EC2 userdata logs check பண்ணு.
- **DB connect fail:** Security group / DB endpoint wrong → `.env` values verify பண்ணு.

---

## 6) Database Configuration
- Uses **Amazon RDS MySQL** via `DATABASE_URL`.
- Example format:
  `mysql+pymysql://erpadmin:password@rds-endpoint:3306/erpdb`
- See `.env.example`.

To initialize schema manually:
```bash
python scripts/init_db.py
```

---

## 7) Deployment Files Explained
- `buildspec.yml`: build + test commands for CodeBuild.
- `appspec.yml`: deployment lifecycle for CodeDeploy.
- `codedeploy/*.sh`: install dependencies, start service, validate health.
- `cloudformation/erp-cicd.yaml`: end-to-end AWS infra.

---

## 8) Notes on Stack Recreation
- Infra definitions are immutable via CloudFormation template.
- Re-running stack with same parameters gives same service topology.
- RDS has `DeletionPolicy: Snapshot` to protect data snapshots on delete.

---

## 9) Local Run (Optional)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app/main.py
```
Open `http://localhost:8000`.
