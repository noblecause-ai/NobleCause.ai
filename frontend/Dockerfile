# Multi-stage build for SvelteKit frontend

# Stage 1: Build the application
FROM node:20 AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json ./

# Clear npm cache and install dependencies
RUN npm cache clean --force
# Remove platform-specific dependency that shouldn't be in dependencies
RUN npm uninstall @rollup/rollup-win32-x64-msvc || true
RUN npm install --force

# Copy source code
COPY . .

# Sync SvelteKit and build the application
RUN npx svelte-kit sync
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine AS production

# Copy the built application from the builder stage
COPY --from=builder /app/.svelte-kit/output/client /usr/share/nginx/html

# Copy custom nginx configuration if needed
# COPY nginx.conf /etc/nginx/nginx.conf

# Create a simple nginx configuration for SPA
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]