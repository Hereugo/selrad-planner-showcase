# ARG NEXT_PUBLIC_BASE_BACKEND_URL

# Install dependencies only when needed
FROM --platform=linux/amd64 node:19-alpine AS deps
ENV NODE_ENV=production
RUN apk add --no-cache libc6-compat
WORKDIR /frontend
COPY package.json package-lock.json ./
RUN npm install husky -g
RUN npm ci

# Rebuild the source code only when needed
FROM --platform=linux/amd64 node:19-alpine AS builder
ENV NODE_ENV=production
WORKDIR /frontend
COPY --from=deps /frontend/node_modules ./node_modules
COPY . .

# ARG NEXT_PUBLIC_BASE_BACKEND_URL

# RUN NEXT_PUBLIC_BASE_BACKEND_URL="" npm run build

RUN npm run build

# Production image, copy all the files and run next
FROM --platform=linux/amd64 node:19-alpine AS runner
WORKDIR /frontend
ENV NODE_ENV=production
# ARG NEXT_PUBLIC_BASE_BACKEND_URL

# You only need to copy next.config.js if you are NOT using the default configuration
COPY --from=builder /frontend/public ./public
COPY --from=builder /frontend/package.json ./package.json

# Automatically leverage output traces to reduce image size 
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /frontend/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /frontend/.next/static ./.next/static

EXPOSE 3000
ENV PORT 3000

CMD ["node", "server.js"]
