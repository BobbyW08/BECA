# Dev Folder Reorganization Plan

**Date**: October 16, 2025  
**Goal**: Clean up c:\dev (BECA repo) - organize loose files, maintain clear structure

---

## 📋 Current Issues

1. **Too many loose files in root** (20+ Python files, batch files, configs)
2. **Mixed concerns** (user scripts, dev scripts, VM management all in root)
3. **Documentation scattered** (multiple md files in root + docs/ folder)
4. **Unclear what's actively used** vs deprecated

---

## 🎯 Proposed Structure

```
c:\dev\                           # BECA Git repository root
├── .git/                         # Git repository (keep as-is)
├── .gitignore                    # Keep in root
├── readme.md                     # Main readme (keep in root)
├── START-BECA.md                 # User-facing quick start (keep in root)
│
├── User Scripts (Keep in root for easy access)
│   ├── start-beca.bat           # Start VM
│   ├── stop-beca.bat            # Stop VM  
│   ├── check-beca.bat           # Check status
│   └── diagnose-beca.bat        # Diagnostic tool
│
├── api/                          # FastAPI backend (keep as-is)
├── frontend/                     # React frontend (keep as-is)
├── src/                          # Python source code (keep as-is)
├── docker/                       # Docker configs (keep as-is)
├── prompts/                      # AI prompts (keep as-is)
│
├── scripts/                      # NEW: Development & deployment scripts
│   ├── vm/                       # VM management scripts
│   │   ├── create_vm.py
│   │   ├── start_beca_vm.py
│   │   ├── get_beca_vm_ip.py
│   │   ├── setup_firewall.py
│   │   └── deploy-to-gcloud.sh
│   ├── deployment/               # Deployment scripts
│   │   ├── deploy-beca-git.bat
│   │   └── setup-new-beca-firewall.bat
│   ├── initialization/           # Setup scripts
│   │   ├── initialize_beca_self_knowledge.py
│   │   ├── initialize_knowledge_system.py
│   │   └── learn_from_self.py
│   └── testing/                  # Test scripts
│       ├── test_meta_learning.py
│       └── quick_start_meta_learning.py
│
├── docs/                         # All documentation
│   ├── README.md                 # Docs index
│   ├── deployment/               # NEW: Deployment docs
│   │   ├── GOOGLE-CLOUD-DEPLOYMENT.md
│   │   └── NEW-DEVELOPMENT-WORKFLOW.md
│   ├── cleanup/                  # NEW: Cleanup/migration docs
│   │   ├── CLEANUP-COMPLETION-SUMMARY.md
│   │   ├── CODEBASE-CLEANUP-ANALYSIS.md
│   │   └── PHASE-3-4-CLEANUP-COMPLETE.md
│   └── (existing docs stay)
│
├── config/                       # NEW: Configuration files
│   ├── cloudbuild.yaml
│   └── docker-compose.yml        # Move root docker-compose here
│
├── data/                         # NEW: Database files
│   └── beca_knowledge.db
│
├── archive/                      # Historical/deprecated files (keep as-is)
│
├── vscode-beca-extension/        # VSCode extension (keep as separate project)
│
└── Folders to Review/Potentially Remove:
    ├── beca/                     # Check if needed
    ├── beca-env/                 # Virtual environment (add to .gitignore)
    ├── cline-reference/          # Check if needed
    ├── google-cloud-sdk/         # Should this be in .gitignore?
    └── .ollama/                  # Should be in .gitignore
```

---

## 📁 Detailed File Moves

### Keep in Root (User-Facing)
- ✅ `.gitignore`
- ✅ `readme.md`
- ✅ `START-BECA.md`
- ✅ `start-beca.bat`
- ✅ `stop-beca.bat`
- ✅ `check-beca.bat`
- ✅ `diagnose-beca.bat`

### Move to scripts/vm/
- `create_vm.py`
- `start_beca_vm.py`
- `get_beca_vm_ip.py`
- `setup_firewall.py`
- `deploy-to-gcloud.sh`

### Move to scripts/deployment/
- `deploy-beca-git.bat`
- `setup-new-beca-firewall.bat`
- `start-beca-improved.bat` (or delete if redundant?)

### Move to scripts/initialization/
- `initialize_beca_self_knowledge.py`
- `initialize_knowledge_system.py`
- `learn_from_self.py`

### Move to scripts/testing/
- `test_meta_learning.py`
- `quick_start_meta_learning.py`

### Move to docs/deployment/
- `NEW-DEVELOPMENT-WORKFLOW.md`
- `docs/GOOGLE-CLOUD-DEPLOYMENT.md` (already there)

### Move to docs/cleanup/
- `CLEANUP-COMPLETION-SUMMARY.md`
- `CODEBASE-CLEANUP-ANALYSIS.md`
- `PHASE-3-4-CLEANUP-COMPLETE.md`
- `docs/CLEANUP-PLAN.md` (already in docs)

### Move to config/
- `cloudbuild.yaml`
- `docker-compose.yml` (root level)

### Move to data/
- `beca_knowledge.db`
- Any other `.db` files

### Folders to Keep As-Is
- ✅ `api/`
- ✅ `frontend/`
- ✅ `src/`
- ✅ `docker/`
- ✅ `prompts/`
- ✅ `archive/`
- ✅ `docs/` (with new subfolders)
- ✅ `vscode-beca-extension/`

### Folders to Review
- `beca/` - Check contents, move or delete
- `beca-env/` - Virtual environment, add to .gitignore
- `cline-reference/` - Check if needed
- `google-cloud-sdk/` - Should be in .gitignore if installed locally
- `.ollama/` - Should be in .gitignore
- `.venv/` - Virtual environment, add to .gitignore
- `.vscode/` - Keep but ensure in .gitignore (user settings)

---

## 🔧 Files That Need Path Updates

After moving files, these need updating:

### Batch Files (if they reference moved scripts)
- `start-beca.bat` - Check for script references
- `stop-beca.bat` - Check for script references
- `check-beca.bat` - Check for script references
- `diagnose-beca.bat` - Check for script references

### Documentation
- `readme.md` - Update any file path references
- `START-BECA.md` - Update script references
- All docs in `docs/` - Update path references

### Python Files
- Check import statements in `src/` files
- Check any hardcoded paths

### Docker/Deployment
- `docker/deploy-gcp.sh` - Check script references
- Any docker-compose files - Check volume/path references

---

## 🚫 .gitignore Additions

Add these to `.gitignore`:
```
# Virtual environments
beca-env/
.venv/
venv/
env/

# Local installations
google-cloud-sdk/
.ollama/

# IDEs
.vscode/
.idea/

# Databases (keep tracked for now, but consider)
# *.db

# Logs
*.log
beca_learning.log
```

---

## ⚠️ Important Considerations

1. **vscode-beca-extension/** 
   - Has its own Git repo: Should we add it to .gitignore and have it as a separate clone?
   - Or keep it as a subfolder (current setup)?
   
2. **Database files**
   - `beca_knowledge.db` - Should this be tracked in Git or .gitignored?
   
3. **Batch files**
   - Some might be redundant (e.g., `start-beca-improved.bat` vs `start-beca.bat`)
   - Review before moving

---

## 📝 Execution Steps

1. ✅ Create new directories
2. ✅ Move files to new locations
3. ✅ Update all path references in code
4. ✅ Update documentation
5. ✅ Update .gitignore
6. ✅ Test user scripts still work
7. ✅ Commit changes

---

## 🎯 Benefits

- **Cleaner root**: Only essential user files
- **Better organization**: Scripts grouped by purpose
- **Clearer documentation**: Organized by topic
- **Easier onboarding**: Clear structure for new contributors
- **Better .gitignore**: Exclude local tools/environments

---

**Ready to proceed?** This plan maintains the current Git repo structure while organizing files into logical directories.
