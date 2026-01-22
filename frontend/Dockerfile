# Frontend Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY public ./public
COPY src ./src

# Build the application
RUN npm run build

# Production server
FROM node:18-alpine

WORKDIR /app

# Install serve
RUN npm install -g serve

# Copy built application from builder
COPY --from=node:18-alpine /app/build ./build

# Expose port
EXPOSE 3000

# Start application
CMD ["serve", "-s", "build", "-l", "3000"]
