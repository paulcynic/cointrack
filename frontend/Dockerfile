# 1. For build React app
FROM node:16.15.1 AS development

# Set working directory
WORKDIR /app

# Copy dependency list
COPY ./app/package.json /app/package.json
COPY ./app/package-lock.json /app/package-lock.json

RUN npm install --location=global

COPY ./app /app

FROM development AS build

RUN npm run build

# 2. For Nginx setup
FROM nginx:alpine

# Copy config nginx
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /usr/share/nginx/html

# Remove default nginx static assets
RUN rm -rf ./*

# Copy static assets from builder stage
COPY --from=build /app/build .

# Containers run nginx with global directives and daemon off
ENTRYPOINT ["nginx", "-g", "daemon off;"]
