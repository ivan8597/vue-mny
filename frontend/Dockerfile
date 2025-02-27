# Этап сборки
FROM node:18-alpine AS build-stage

# Установка рабочей директории
WORKDIR /app

# Копирование package.json и package-lock.json
COPY package*.json ./

# Установка зависимостей
RUN npm install

# Копирование исходного кода
COPY . .

# Временно отключаем проверку типов при сборке
ENV VITE_DISABLE_TYPE_CHECK=true

# Сборка приложения
RUN npm run build

# Этап production
FROM nginx:stable-alpine AS production-stage

# Копирование собранного приложения
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Копирование nginx конфигурации
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 