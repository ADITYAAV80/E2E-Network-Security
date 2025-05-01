# --- Stage 1: Build the app ---
FROM node:18 AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build


# --- Stage 2: Serve the app ---
FROM node:18-slim

WORKDIR /app
# Install only serve
RUN npm install -g serve

# Copy only the build output from builder stage
COPY --from=builder /app/dist ./dist

EXPOSE 5173
CMD ["serve", "-s", "dist", "-l", "5173"]
