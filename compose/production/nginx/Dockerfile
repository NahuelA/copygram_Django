FROM nginx

COPY ./compose/production/nginx/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /nginx