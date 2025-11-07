/**
 * MCP Server for BECA
 * Exposes BECA's 39+ tools as Model Context Protocol resources
 * Allows Claude Desktop/API to call BECA tools directly
 */

const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 8080;
const BECA_API_URL = process.env.BECA_API_URL || 'http://beca-backend:8000';

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Authentication middleware (simple token-based)
const authenticate = (req, res, next) => {
  const token = req.headers['authorization'];
  const expectedToken = process.env.MCP_AUTH_TOKEN || 'beca-default-token';
  
  if (token !== `Bearer ${expectedToken}`) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
};

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'beca-mcp-server' });
});

// MCP Protocol Endpoints

// List available tools/resources
app.get('/mcp/tools', authenticate, async (req, res) => {
  try {
    const tools = {
      tools: [
        // File Operations
        {
          name: 'read_file',
          description: 'Read contents of a file',
          parameters: {
            file_path: { type: 'string', required: true, description: 'Path to file' }
          }
        },
        {
          name: 'write_file',
          description: 'Write or update a file',
          parameters: {
            file_path: { type: 'string', required: true, description: 'Path to file' },
            content: { type: 'string', required: true, description: 'File content' }
          }
        },
        {
          name: 'list_files',
          description: 'List files in directory',
          parameters: {
            directory_path: { type: 'string', required: true, description: 'Directory path' }
          }
        },
        {
          name: 'find_in_files',
          description: 'Search for text across files',
          parameters: {
            search_term: { type: 'string', required: true, description: 'Text to search' },
            directory: { type: 'string', required: false, description: 'Directory to search' },
            pattern: { type: 'string', required: false, description: 'File pattern (e.g., *.py)' }
          }
        },
        
        // Git Operations
        {
          name: 'git_status',
          description: 'Show git repository status',
          parameters: {}
        },
        {
          name: 'git_diff',
          description: 'Show git diff for file',
          parameters: {
            file_path: { type: 'string', required: false, description: 'Specific file to diff' }
          }
        },
        {
          name: 'git_commit',
          description: 'Commit changes with message',
          parameters: {
            message: { type: 'string', required: true, description: 'Commit message' }
          }
        },
        
        // Code Analysis
        {
          name: 'analyze_code',
          description: 'Analyze code quality and metrics',
          parameters: {
            file_path: { type: 'string', required: true, description: 'File to analyze' }
          }
        },
        {
          name: 'find_bugs',
          description: 'Detect potential bugs in code',
          parameters: {
            file_path: { type: 'string', required: true, description: 'File to check' }
          }
        },
        
        // Web & Research
        {
          name: 'web_search',
          description: 'Search the web using DuckDuckGo',
          parameters: {
            query: { type: 'string', required: true, description: 'Search query' },
            max_results: { type: 'number', required: false, description: 'Max results (default: 5)' }
          }
        },
        {
          name: 'fetch_url',
          description: 'Fetch content from URL',
          parameters: {
            url: { type: 'string', required: true, description: 'URL to fetch' }
          }
        },
        
        // Memory & Knowledge
        {
          name: 'search_knowledge',
          description: 'Search BECA knowledge base',
          parameters: {
            query: { type: 'string', required: true, description: 'Search query' },
            category: { type: 'string', required: false, description: 'Knowledge category' }
          }
        },
        {
          name: 'remember_preference',
          description: 'Save user preference',
          parameters: {
            category: { type: 'string', required: true, description: 'Preference category' },
            key: { type: 'string', required: true, description: 'Preference key' },
            value: { type: 'string', required: true, description: 'Preference value' }
          }
        },
        {
          name: 'recall_preferences',
          description: 'Get all saved preferences',
          parameters: {}
        },
        
        // Code Generation
        {
          name: 'create_react_app',
          description: 'Create a React application',
          parameters: {
            app_name: { type: 'string', required: true, description: 'Application name' }
          }
        },
        {
          name: 'create_project_from_template',
          description: 'Create project from template',
          parameters: {
            type: { type: 'string', required: true, description: 'Template type: react-vite, flask-api, fastapi, python-cli' },
            name: { type: 'string', required: true, description: 'Project name' }
          }
        }
      ]
    };
    
    res.json(tools);
  } catch (error) {
    console.error('Error listing tools:', error);
    res.status(500).json({ error: 'Failed to list tools' });
  }
});

// Execute a tool
app.post('/mcp/execute', authenticate, async (req, res) => {
  try {
    const { tool_name, parameters } = req.body;
    
    if (!tool_name) {
      return res.status(400).json({ error: 'tool_name is required' });
    }
    
    console.log(`Executing tool: ${tool_name}`, parameters);
    
    // Forward request to BECA backend
    const response = await axios.post(`${BECA_API_URL}/api/tool`, {
      tool: tool_name,
      params: parameters || {}
    }, {
      timeout: 30000 // 30 second timeout
    });
    
    res.json({
      success: true,
      tool: tool_name,
      result: response.data
    });
    
  } catch (error) {
    console.error('Error executing tool:', error.message);
    res.status(500).json({
      success: false,
      error: error.message,
      details: error.response?.data || 'Tool execution failed'
    });
  }
});

// Get BECA status
app.get('/mcp/status', authenticate, async (req, res) => {
  try {
    const response = await axios.get(`${BECA_API_URL}/api/status`, {
      timeout: 5000
    });
    
    res.json({
      beca_status: 'connected',
      details: response.data
    });
  } catch (error) {
    res.status(503).json({
      beca_status: 'disconnected',
      error: 'Cannot connect to BECA backend'
    });
  }
});

// MCP Resources endpoint
app.get('/mcp/resources', authenticate, async (req, res) => {
  try {
    const resources = {
      resources: [
        {
          name: 'beca_memory',
          description: 'BECA conversation memory and preferences',
          uri: 'beca://memory/all',
          type: 'database'
        },
        {
          name: 'beca_knowledge',
          description: 'BECA knowledge base',
          uri: 'beca://knowledge/all',
          type: 'database'
        },
        {
          name: 'learning_queue',
          description: 'Autonomous learning queue',
          uri: 'beca://learning/queue',
          type: 'queue'
        },
        {
          name: 'project_files',
          description: 'Current project file tree',
          uri: 'beca://workspace/files',
          type: 'filesystem'
        }
      ]
    };
    
    res.json(resources);
  } catch (error) {
    console.error('Error listing resources:', error);
    res.status(500).json({ error: 'Failed to list resources' });
  }
});

// Access a resource
app.get('/mcp/resources/:resource_name', authenticate, async (req, res) => {
  try {
    const { resource_name } = req.params;
    
    // Forward to BECA to fetch resource
    const response = await axios.get(`${BECA_API_URL}/api/resource/${resource_name}`, {
      timeout: 10000
    });
    
    res.json(response.data);
  } catch (error) {
    console.error('Error accessing resource:', error.message);
    res.status(500).json({ error: 'Failed to access resource' });
  }
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log('==========================================');
  console.log('🚀 BECA MCP Server Started');
  console.log('==========================================');
  console.log(`Port: ${PORT}`);
  console.log(`BECA Backend: ${BECA_API_URL}`);
  console.log(`Auth: ${process.env.MCP_AUTH_TOKEN ? 'Enabled' : 'Default token'}`);
  console.log('==========================================');
  console.log('\nEndpoints:');
  console.log('  GET  /health              - Health check');
  console.log('  GET  /mcp/tools           - List available tools');
  console.log('  POST /mcp/execute         - Execute a tool');
  console.log('  GET  /mcp/status          - BECA status');
  console.log('  GET  /mcp/resources       - List resources');
  console.log('  GET  /mcp/resources/:name - Access resource');
  console.log('==========================================\n');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully...');
  process.exit(0);
});
