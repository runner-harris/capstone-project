# Use the official Node.js image as the base image
FROM node:16

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json and install dependencies
COPY package*.json ./
RUN npm ci

# Copy the rest of the application code
COPY . .

# Build the Angular app
RUN npm run build

# Use an Nginx image to serve the static files
FROM nginx:1.21

# Copy the build output to the Nginx default public folder
COPY --from=0 /app/dist/coordinator-front /usr/share/nginx/html

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf
