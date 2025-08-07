# Build stage
FROM node:18-alpine AS build

# Build arguments for environment variables
ARG REACT_APP_AUTH_BACKEND_URL=http://localhost:8000
ARG REACT_APP_HYDRA_PUBLIC_URL=http://localhost:4444

# Set environment variables from build args
ENV REACT_APP_AUTH_BACKEND_URL=$REACT_APP_AUTH_BACKEND_URL
ENV REACT_APP_HYDRA_PUBLIC_URL=$REACT_APP_HYDRA_PUBLIC_URL

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including dev dependencies for build)
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:18-alpine AS production

WORKDIR /app

# Install serve globally
RUN npm install -g serve

# Copy built application from build stage
COPY --from=build /app/build ./build

# Expose port
EXPOSE 3000

# Start the application
CMD ["serve", "-s", "build", "-l", "3000"]
