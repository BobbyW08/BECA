# BECA Cleanup Plan

## Files to Remove

### Duplicate/Old Documentation
- ✅ beca_enhancements.md (old)
- ✅ BECA_IMPROVEMENTS.md (old)
- ✅ BECA-FRONTEND-IMPLEMENTATION.md (moved to docs/)
- ✅ LANGCHAIN-AGENT-FIX.md (old)
- ✅ PROJECT-SEPARATION-SUMMARY.md (old)
- ✅ GOOGLE-CLOUD-DEPLOYMENT.md (duplicate)

### Test/Development Files
- ✅ test_meta_learning.py
- ✅ quick_start_meta_learning.py
- ✅ check-beca.bat

### One-time Setup Scripts (No Longer Needed)
- ✅ initialize_beca_self_knowledge.py
- ✅ initialize_knowledge_system.py
- ✅ learn_from_self.py (integrated into system)

### Cloud Deployment Scripts (Optional - Keep in cloud-deployment/)
- create_vm.py
- setup_firewall.py
- start_beca_vm.py
- get_beca_vm_ip.py
- deploy-to-gcloud.sh
- cloudbuild.yaml

### Large Reference Directories (Remove)
- ✅ vscode-beca-extension/ (move to separate repo)
- ✅ cline-reference/ (reference code)
- ✅ beca/ (duplicate)
- ✅ google-cloud-sdk/ (large SDK)
- ✅ frontend/ (separate project)
- ✅ api/ (separate project)

### Superseded Files
- ✅ beca_gui.py (use beca_gui_enhanced.py instead)
- ✅ docker-compose.yml (root - keep one in docker/)

## Files to Keep

### Essential
- beca_gui_enhanced.py (main GUI)
- start-beca.bat
- stop-beca.bat
- START-BECA.md
- requirements.txt
- readme.md
- .gitignore

### Directories
- src/ (all source code)
- docs/ (documentation)
- prompts/ (useful)
- docker/ (deployment)
- beca-env/ (virtual environment)
- uploads/ (file uploads)

### Databases
- beca_knowledge.db
- beca_memory.db
- beca_learning.log

## Actions

1. Remove files listed above
2. Create cloud-deployment/ folder for VM scripts
3. Update .gitignore
4. Create simple QUICK-START.md
5. Commit cleanup
