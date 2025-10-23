# Stage 1: Build the Theia application
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json yarn.lock* ./
COPY browser-app/package.json ./browser-app/
COPY beca-extension/package.json ./beca-extension/

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy source files
COPY . .

# Build the BECA extension
WORKDIR /app/beca-extension
RUN yarn build

# Build the browser app
WORKDIR /app/browser-app
RUN yarn build

# Stage 2: Production image
FROM node:18-alpine

WORKDIR /app

# Install only production dependencies
COPY --from=builder /app/package.json /app/yarn.lock* ./
COPY --from=builder /app/browser-app/package.json ./browser-app/
COPY --from=builder /app/beca-extension/package.json ./beca-extension/

RUN yarn install --production --frozen-lockfile

# Copy built application
COPY --from=builder /app/beca-extension/lib ./beca-extension/lib
COPY --from=builder /app/browser-app/lib ./browser-app/lib
COPY --from=builder /app/browser-app/src-gen ./browser-app/src-gen

# Set environment variables
ENV NODE_ENV=production
ENV BECA_API_URL=http://beca-backend:8000

# Expose Theia port
EXPOSE 3000

# Start Theia
WORKDIR /app/browser-app
CMD ["yarn", "start", "--hostname=0.0.0.0", "--port=3000"]
