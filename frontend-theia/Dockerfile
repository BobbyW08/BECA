# Stage 1: Build the Theia application
FROM node:20-alpine AS builder

# Install git, python, and build dependencies (required by some node modules)
RUN apk add --no-cache git python3 py3-setuptools make g++

WORKDIR /app

# Copy package files
COPY package.json yarn.lock* ./
COPY browser-app/package.json ./browser-app/

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy source files
COPY . .

# Build the browser app
WORKDIR /app/browser-app
RUN yarn build

# Stage 2: Production image
FROM node:20-alpine

# Install git, python, and build tools for production dependencies
RUN apk add --no-cache git python3 py3-setuptools make g++

WORKDIR /app

# Install only production dependencies
COPY --from=builder /app/package.json /app/yarn.lock* ./
COPY --from=builder /app/browser-app/package.json ./browser-app/

# Install theia CLI globally for production
RUN yarn global add @theia/cli@^1.43.0

RUN yarn install --production --frozen-lockfile

# Copy built application
COPY --from=builder /app/browser-app/lib ./browser-app/lib
COPY --from=builder /app/browser-app/src-gen ./browser-app/src-gen

# Set environment variables
ENV NODE_ENV=production
ENV BECA_API_URL=http://beca-backend:8000

# Expose Theia port
EXPOSE 3000

# Start Theia
WORKDIR /app/browser-app
CMD ["yarn", "start"]
