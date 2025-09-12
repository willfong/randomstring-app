FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production && npm cache clean --force

FROM node:22-alpine
WORKDIR /app
COPY --from=build /app/node_modules ./node_modules
COPY index.mjs ./
EXPOSE 3000
CMD ["node", "--max-old-space-size=64", "--gc-interval=100", "index.mjs"]
