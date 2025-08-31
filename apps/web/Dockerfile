FROM node:18-alpine

# sharp/Image optimization on alpine needs this
RUN apk add --no-cache libc6-compat

WORKDIR /app

# Install only the web app deps
COPY apps/web/package*.json ./
RUN npm install --legacy-peer-deps

# Copy the rest of the app
COPY apps/web/ ./

# Build Next.js
RUN npm run build

EXPOSE 3000

# Next.js will read NEXT_PUBLIC_* at runtime; docker-compose sets it
ENV NEXT_TELEMETRY_DISABLED=1

CMD ["npm", "run", "start"]
