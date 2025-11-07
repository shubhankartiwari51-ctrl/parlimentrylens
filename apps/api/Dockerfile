# 🧱 Base Image
FROM node:20-bullseye

# Set working directory
WORKDIR /app

# 🧠 Fix yt-dlp-exec error by installing Python3 + tools
RUN apt-get update && apt-get install -y python3 make g++ && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Expose backend port
EXPOSE 8000

# Run development server
CMD ["npx", "tsx", "watch", "src/index.ts"]
