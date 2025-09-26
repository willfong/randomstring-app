FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production && \
    npm cache clean --force && \
    rm -rf /tmp/* /var/cache/apk/* /usr/share/man /usr/share/doc

FROM node:22-alpine
# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodeuser -u 1001 -G nodejs

WORKDIR /app

# Copy files and set ownership to non-root user
COPY --from=build --chown=nodeuser:nodejs /app/node_modules ./node_modules
COPY --chown=nodeuser:nodejs index.mjs ./

# Switch to non-root user
USER nodeuser

EXPOSE 3000
CMD ["node", "--max-old-space-size=64", "--gc-interval=100", "index.mjs"]
