#!/bin/bash
# Create systemd service for BECA Docker containers auto-start

cat > /tmp/docker-compose-beca.service <<'EOF'
[Unit]
Description=Docker Compose BECA Application Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/beca
ExecStartPre=/bin/sleep 10
ExecStartPre=/usr/bin/systemctl stop ollama
ExecStart=/usr/bin/docker-compose -f docker/docker-compose.yml up -d
ExecStop=/usr/bin/docker-compose -f docker/docker-compose.yml down
TimeoutStartSec=300

[Install]
WantedBy=multi-user.target
EOF

# Move to systemd directory
sudo mv /tmp/docker-compose-beca.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable docker-compose-beca.service

# Show status
sudo systemctl status docker-compose-beca.service

echo ""
echo "✅ Auto-start service created and enabled!"
echo "BECA containers will now automatically start when the VM boots."
