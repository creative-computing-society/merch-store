create:
	sudo docker-compose up --build -d

destroy:
	sudo docker-compose down

recreateall:
	make destroy
	make create

redeploy:
	sudo docker stop merch-store_merchstoreapi_1
	sudo docker rm merch-store_merchstoreapi_1
	git pull
	sudo docker-compose up --no-recreate --build -d
