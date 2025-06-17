all: up build

all-log:
	docker compose up --build

up:
	docker compose up -d

build:
	docker compose build

down:
	-@docker compose down -v

clean:
	-@docker rm -f $$(docker container ls -aq)
	-@docker rmi -f $$(docker images -q)
	-@docker network rm services
	-@docker volume rm -f $$(docker volume ls -q)

fclean: clean
	-@yes | docker system prune -a
	-@yes | docker image prune -a
	-@yes | docker volume prune
	-@yes | docker network prune
	-@yes | docker container prune

logs:
	docker compose logs -f

backend:
	docker exec -it backend /bin/sh

frontend:
	docker exec -it frontend /bin/sh

database:
	docker exec -it mongodb /bin/sh

nginx:
	docker exec -it nginx /bin/sh

re: down all-log

.PHONY: all down clean fclean logs re all-log backend frontend database nginx up build
