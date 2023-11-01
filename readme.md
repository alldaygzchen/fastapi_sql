# download docker desktop instruction
https://www.youtube.com/watch?v=AAWNQ2wDVAg  

# run code in local
uvicorn app.main:app --reload  

# useful docker command 
docker-compose -f docker-compose-dev.yml build 
docker-compose -f docker-compose-dev.yml up -d
docker-compose -f docker-compose-dev.yml down  
docker ps -a 
docker logs 22cefa45bbd5  
docker volume rm fastapi_sql_postgres-db   
docker images  