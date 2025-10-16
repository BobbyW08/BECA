# BECA MCP Integration Guide

Connect Claude Desktop or Cline extension to BECA's MCP server to access all 39+ tools as MCP resources.

## 🎯 What is MCP?

**Model Context Protocol (MCP)** is a standard way for AI assistants like Claude to access external tools and data sources. BECA's MCP server exposes all of BECA's capabilities (file operations, git commands, code analysis, memory, knowledge search, etc.) so Claude can use them directly.

## 🔧 Architecture

```
┌──────────────────┐          ┌──────────────────┐
│  Your Computer   │          │  GCP VM (Docker) │
│                  │          │                  │
│  ┌────────────┐ │          │  ┌────────────┐  │
│  │  VS Code   │ │          │  │ MCP Server │  │
│  │  + Cline   │ │──MCP───▶ │  │ Port 8080  │  │
│  └────────────┘ │          │  └──────┬─────┘  │
│                  │          │         │        │
│  ┌────────────┐ │          │  ┌──────▼─────┐  │
│  │  Claude    │ │          │  │ BECA Agent │  │
│  │  Desktop   │ │──MCP───▶ │  │ + Tools    │  │
│  └────────────┘ │          │  └────────────┘  │
└──────────────────┘          └──────────────────┘
```

## 📋 Prerequisites

- BECA Docker stack deployed and running
- MCP server accessible (check with `./docker/status-beca.sh`)
- Your MCP auth token (from `docker/.env`)

## 🚀 Claude Desktop Setup

### 1. Get Your MCP Server URL

```bash
# Get your VM's external IP
./docker/status-beca.sh

# Your MCP server URL will be:
http://YOUR_VM_IP:8080
```

### 2. Get Your Auth Token

```bash
# View your token
cat docker/.env | grep MCP_AUTH_TOKEN

# Or generate a new one
openssl rand -hex 32
```

### 3. Configure Claude Desktop

**Location of config file:**
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Add to config:**

```json
{
  "mcpServers": {
    "beca": {
      "url": "http://YOUR_VM_IP:8080/mcp",
      "transport": "http",
      "headers": {
        "Authorization": "Bearer YOUR_MCP_AUTH_TOKEN"
      }
    }
  }
}
```

### 4. Restart Claude Desktop

Close and reopen Claude Desktop to load the new configuration.

### 5. Test the Connection

In Claude Desktop, try:
```
Can you list the available MCP tools from BECA?
```

Claude should respond with a list of BECA's tools.

## 🔌 Cline Extension Setup

### 1. Install Cline Extension

If not already installed:
```bash
code --install-extension saoudrizwan.claude-dev
```

### 2. Configure MCP in Cline

1. Open VS Code
2. Click the Cline icon in the sidebar
3. Click the gear icon (⚙️) for settings
4. Navigate to **MCP Servers** section
5. Click **Add Server**

**Server Configuration:**

```json
{
  "name": "beca",
  "url": "http://YOUR_VM_IP:8080/mcp",
  "transport": "http",
  "headers": {
    "Authorization": "Bearer YOUR_MCP_AUTH_TOKEN"
  }
}
```

### 3. Enable BECA MCP Server

In Cline's MCP servers list, toggle the BECA server to **enabled**.

### 4. Test in Cline

Open Cline chat and try:
```
Use the BECA MCP server to list files in the current directory
```

## 🛠️ Available MCP Tools

### File Operations (4 tools)

```javascript
// Read file contents
read_file(file_path: string)

// Write or update file
write_file(file_path: string, content: string)

// List directory contents
list_files(directory_path: string)

// Search across files
find_in_files(search_term: string, directory?: string, pattern?: string)
```

### Git Operations (3 tools)

```javascript
// Show git status
git_status()

// Show changes (diff)
git_diff(file_path?: string)

// Commit changes
git_commit(message: string)
```

### Code Analysis (2 tools)

```javascript
// Analyze code quality
analyze_code(file_path: string)

// Detect potential bugs
find_bugs(file_path: string)
```

### Web & Research (2 tools)

```javascript
// Search the web
web_search(query: string, max_results?: number)

// Fetch URL content
fetch_url(url: string)
```

### Memory & Knowledge (3 tools)

```javascript
// Search BECA's knowledge base
search_knowledge(query: string, category?: string)

// Save a preference
remember_preference(category: string, key: string, value: string)

// Get all preferences
recall_preferences()
```

### Code Generation (2 tools)

```javascript
// Create React app
create_react_app(app_name: string)

// Create from template
create_project_from_template(
  type: 'react-vite' | 'flask-api' | 'fastapi' | 'python-cli',
  name: string
)
```

## 📚 MCP Resources

BECA also exposes data resources via MCP:

### Available Resources

```javascript
// BECA memory (conversations, preferences)
beca://memory/all

// BECA knowledge base
beca://knowledge/all

// Autonomous learning queue
beca://learning/queue

// Project file tree
beca://workspace/files
```

### Accessing Resources

**In Claude Desktop:**
```
Can you access the beca://memory/all resource and show my preferences?
```

**In Cline:**
```
Use MCP to access beca://knowledge/all and search for React patterns
```

## 💡 Example Workflows

### Workflow 1: File Management

```
Claude/Cline: "Use BECA MCP to list all Python files in the src directory"
→ Uses list_files(directory_path: 'src', pattern: '*.py')

Claude/Cline: "Read the contents of src/main.py"
→ Uses read_file(file_path: 'src/main.py')

Claude/Cline: "Add a new function to handle authentication"
→ Uses write_file() to update the file
```

### Workflow 2: Code Analysis

```
Claude/Cline: "Analyze the code quality of api/routes.py using BECA"
→ Uses analyze_code(file_path: 'api/routes.py')

Claude/Cline: "Find any potential bugs in the authentication module"
→ Uses find_bugs(file_path: 'auth/auth.py')
```

### Workflow 3: Knowledge Search

```
Claude/Cline: "Search BECA's knowledge base for FastAPI examples"
→ Uses search_knowledge(query: 'FastAPI', category: 'code_patterns')

Claude/Cline: "Remember that I prefer TypeScript over JavaScript"
→ Uses remember_preference(category: 'language', key: 'frontend', value: 'TypeScript')
```

### Workflow 4: Project Scaffolding

```
Claude/Cline: "Use BECA to create a new React app called 'dashboard'"
→ Uses create_react_app(app_name: 'dashboard')

Claude/Cline: "Create a Flask API project named 'backend-api'"
→ Uses create_project_from_template(type: 'flask-api', name: 'backend-api')
```

## 🔐 Security Best Practices

### 1. Use Strong Auth Tokens

```bash
# Generate a strong token
openssl rand -hex 32

# Update in docker/.env
MCP_AUTH_TOKEN=your-very-long-secure-token
```

### 2. Restrict IP Access

```bash
# Update firewall to only allow your IP
gcloud compute firewall-rules update beca-mcp \
  --source-ranges=YOUR_IP/32
```

### 3. Use HTTPS (Production)

For production deployments:
1. Get a domain name
2. Configure Let's Encrypt SSL
3. Use nginx reverse proxy (included in docker-compose.yml)
4. Access via `https://your-domain.com/mcp/`

### 4. Rotate Tokens Regularly

```bash
# Generate new token
NEW_TOKEN=$(openssl rand -hex 32)

# Update .env
echo "MCP_AUTH_TOKEN=$NEW_TOKEN" >> docker/.env

# Restart MCP server
gcloud compute ssh beca-ollama --zone=us-central1-b \
  --command="sudo docker-compose -f /opt/beca/docker/docker-compose.yml restart mcp-server"

# Update Claude/Cline configs with new token
```

## 🛠️ Troubleshooting

### MCP Server Not Responding

```bash
# Check if MCP server is running
./docker/status-beca.sh

# Check MCP server health
curl http://YOUR_VM_IP:8080/health

# View MCP server logs
gcloud compute ssh beca-ollama --zone=us-central1-b \
  --command="sudo docker logs mcp-server -f"
```

### Authentication Errors

```bash
# Verify token matches
cat docker/.env | grep MCP_AUTH_TOKEN

# Test with curl
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://YOUR_VM_IP:8080/mcp/tools
```

### Connection Timeout

```bash
# Check firewall rules
gcloud compute firewall-rules list --filter="name~beca-mcp"

# Verify your IP is allowed
curl ifconfig.me

# Update firewall if needed
gcloud compute firewall-rules update beca-mcp \
  --source-ranges=YOUR_NEW_IP/32
```

### Tools Not Available

```bash
# Check BECA agent is running
./docker/status-beca.sh

# Test BECA backend directly
curl http://YOUR_VM_IP:7860/api/status

# Restart entire stack
gcloud compute ssh beca-ollama --zone=us-central1-b \
  --command="sudo docker-compose -f /opt/beca/docker/docker-compose.yml restart"
```

## 📊 Monitoring MCP Usage

### View MCP Server Logs

```bash
# Real-time logs
gcloud compute ssh beca-ollama --zone=us-central1-b \
  --command="sudo docker logs mcp-server -f"

# Last 100 lines
gcloud compute ssh beca-ollama --zone=us-central1-b \
  --command="sudo docker logs mcp-server --tail 100"
```

### Check Tool Usage

The MCP server logs show:
- Tool calls from Claude/Cline
- Authentication attempts
- Errors and responses
- Performance metrics

## 🚀 Advanced Configuration

### Custom Tool Endpoints

Modify `docker/mcp-server.js` to add custom tool mappings:

```javascript
// Add new tool
{
  name: 'my_custom_tool',
  description: 'Does something custom',
  parameters: {
    param1: { type: 'string', required: true }
  }
}
```

### Rate Limiting

MCP server includes rate limiting in `docker/nginx.conf`:

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=5r/s;
```

Adjust as needed for your usage patterns.

### CORS Configuration

For browser-based access, CORS is already enabled in `docker/mcp-server.js`. Modify if needed:

```javascript
app.use(cors({
  origin: 'https://your-allowed-domain.com',
  methods: ['GET', 'POST']
}));
```

## 📚 Additional Resources

- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Claude Desktop Documentation](https://docs.anthropic.com/claude/docs)
- [Cline Extension Docs](https://github.com/saoudrizwan/claude-dev)
- [BECA Tools Reference](../readme.md#tools--capabilities)

## 🆘 Getting Help

If you encounter issues:
1. Check MCP server logs
2. Verify authentication tokens
3. Confirm firewall rules
4. Test with curl commands
5. Review Claude/Cline console for errors

## 📝 Example Config Files

### Complete Claude Desktop Config

```json
{
  "mcpServers": {
    "beca": {
      "url": "http://34.46.140.140:8080/mcp",
      "transport": "http",
      "headers": {
        "Authorization": "Bearer abc123def456..."
      }
    }
  },
  "apiKey": "your-claude-api-key"
}
```

### Complete Cline MCP Config

```json
{
  "mcpServers": [
    {
      "name": "beca",
      "url": "http://34.46.140.140:8080/mcp",
      "transport": "http",
      "headers": {
        "Authorization": "Bearer abc123def456..."
      },
      "enabled": true
    }
  ]
}
```

---

**Ready to use BECA with Claude/Cline? Follow the setup steps above and start building!** 🚀
