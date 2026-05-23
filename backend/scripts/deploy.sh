docker build -t enterprise-assistant-backend:$CI_COMMIT_SHA -f backend/Dockerfile backend/
docker run -d --name enterprise-assistant-backend \
  -e DB_HOST=$DB_HOST \
  -e DB_PORT=$DB_PORT \
  -e DB_USER=$DB_USER \
  -e DB_PASSWORD=$DB_PASSWORD \
  -e DB_NAME=$DB_NAME \
  -e SECRET_KEY=$SECRET_KEY \
  -e JWT_SECRET=$JWT_SECRET \
  -p 5000:5000 \
  enterprise-assistant-backend:$CI_COMMIT_SHA

docker ps | grep enterprise-assistant-backend || { echo "Container failed to start"; docker logs enterprise-assistant-backend; exit 1; }