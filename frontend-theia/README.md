# BECA Theia IDE Frontend

Eclipse Theia-based IDE with integrated BECA chat assistant.

## Overview

This frontend replaces the React-based UI with a full-featured IDE powered by Eclipse Theia, providing:
- Complete VS Code-like IDE experience
- Integrated BECA chat panel with Plan/Act modes
- "Follow BECA" mode - auto-opens files that BECA modifies
- Built-in terminal, file explorer, and code editor
- Direct workspace access (C:/dev mounted)

## Structure

```
frontend-theia/
├── browser-app/          # Theia browser application
│   └── package.json      # App dependencies and Theia configuration
├── beca-extension/       # Custom BECA extension
│   ├── src/
│   │   └── browser/
│   │       ├── beca-api-service.ts           # Backend API client
│   │       ├── beca-chat-widget.tsx          # Chat UI component
│   │       ├── beca-view-contribution.ts     # Theia integration
│   │       ├── beca-extension-frontend-module.ts  # Module registration
│   │       └── style/
│   │           └── beca-chat.css             # Chat styles
│   ├── package.json      # Extension dependencies
│   └── tsconfig.json     # TypeScript configuration
├── Dockerfile            # Container build configuration
├── .dockerignore         # Docker build exclusions
└── package.json          # Workspace root configuration
```

## Features

### 1. BECA Chat Panel
- **Location**: Right sidebar (default)
- **Plan/Act Toggle**: Switch between planning and execution modes
- **Follow Mode**: Auto-opens files BECA modifies (eye icon)
- **Chat History**: Persistent conversation history
- **Real-time**: Direct connection to BECA backend API

### 2. File Tracking
When Follow mode is enabled (default), files that BECA modifies will automatically:
- Open in the editor
- Get focused/revealed
- Allow you to review changes in real-time

### 3. Integrated Terminal
- Full terminal access built into Theia
- Execute commands, run scripts
- Multiple terminal instances supported

## Development

### Local Development (without Docker)

```bash
# Install dependencies
cd frontend-theia
yarn install

# Build the extension
cd beca-extension
yarn build

# Build and start the IDE
cd ../browser-app
yarn build
yarn start
```

Access at: http://localhost:3000

### Docker Development

```bash
# Build the frontend image
cd docker
docker-compose build beca-frontend

# Start the frontend (with backend)
docker-compose up beca-frontend
```

Access at: http://localhost:3000

## Configuration

### Environment Variables

- `BECA_API_URL`: Backend API URL (default: http://beca-backend:8000)
- `NODE_ENV`: Environment mode (production/development)

### Theia Preferences

Default preferences (can be changed in IDE):
- Auto-save: After delay
- Font size: 14px
- Word wrap: On
- Theme: Dark
- Minimap: Enabled

## API Integration

The extension connects to the BECA backend at:
- Chat: POST `/chat`
- Status: GET `/status`
- History: GET `/chat/history`
- Files: POST `/files/read`, `/files/write`, `/files/list`

All requests include proper error handling and timeout (5 minutes).

## Troubleshooting

### Extension not loading
```bash
# Rebuild the extension
cd beca-extension
yarn clean
yarn build

# Rebuild the app
cd ../browser-app
yarn clean
yarn build
```

### Chat not connecting
1. Check BECA backend is running: http://localhost:8000/health
2. Verify BECA_API_URL environment variable
3. Check browser console for errors (F12)

### TypeScript errors during build
```bash
# Clear all and reinstall
rm -rf node_modules beca-extension/node_modules browser-app/node_modules
rm -rf beca-extension/lib browser-app/lib browser-app/src-gen
yarn install
yarn build
```

## Phase 2 Completion

This completes Phase 2 of the BECA IDE implementation:
- ✅ Eclipse Theia setup
- ✅ BECA extension with chat panel
- ✅ File tracking ("Follow BECA" mode)
- ✅ Backend API integration
- ✅ Docker configuration
- ✅ Terminal integration (built into Theia)

## Next Steps

1. Deploy to GCP VM
2. Test full workflow
3. Performance optimization if needed
4. Add more IDE features (git integration, debugging, etc.)
