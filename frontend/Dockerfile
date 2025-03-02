# Этап сборки
FROM node:18 as build-stage

# Используем кэширование npm для ускорения сборки
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Копируем только нужные файлы, избегая node_modules
COPY src/ src/
COPY public/ public/
COPY index.html .
COPY *.json ./
COPY vite.config.* .

# Временно отключаем проверку типов при сборке
ENV VITE_DISABLE_TYPE_CHECK=true

# Сборка приложения
RUN npm run build

# Этап production
FROM nginx:stable-alpine as production-stage

# Копирование собранного приложения
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Копирование nginx конфигурации
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 