# Use official Node.js image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your code
COPY . .

# Build the React app
RUN npm run build

# Serve the build using a static file server
RUN npm install -g serve

# Expose port 5173
EXPOSE 5173

# Run the production build with serve
CMD ["serve", "-s", "dist", "-l", "5173"]
# CMD ["npm","run","dev"]