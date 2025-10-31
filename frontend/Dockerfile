# syntax=docker/dockerfile:1

# Use an official Node image for building and running Vite
FROM node:20-alpine AS base

# Set working directory
WORKDIR /app

# Copy only package files first for dependency caching
COPY package*.json ./

# Use npm ci for deterministic builds; cache dependencies
RUN npm ci

# Copy the rest of the project
COPY . .

# Expose the Vite development server port
EXPOSE 5173

# Run Vite dev server (fast refresh enabled)
CMD ["npm", "run", "dev"]