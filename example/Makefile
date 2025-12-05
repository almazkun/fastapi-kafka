build: 
	docker compose build

pull: 
	docker compose pull

up: kafka
	sleep 2
	docker compose up -d --build

logs:
	docker compose logs -n 100 -f case_context case_fetcher

kafka:
	docker compose up -d kafka

down:
	docker compose down -v

ps:
	docker compose ps -a 