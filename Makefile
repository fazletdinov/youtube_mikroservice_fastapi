.PHONY: all up up-users up-video up-likes up-comment up-chat
.PHONY: stop stop-likes stop-video stop-users stop-comment stop-chat
.PHONY: down down-likes down-video down-users down-comment down-chat
.PHONY: down-v down-likes-v down-video-v down-users-v down-comment-v down-chat-v
.PHONY: migrate-video migrate-likes migrate-users migrate-comment migrate-chat
.PHONY: network network-delete

USERS_COMPOSE_FILE := users/docker-compose.users.yml
VIDEO_COMPOSE_FILE := video/docker-compose.video.yml
LIKES_COMPOSE_FILE := likes/docker-compose.likes.yml
COMMENT_COMPOSE_FILE := comment/docker-compose.comment.yml
CHAT_COMPOSE_FILE := chat/docker-compose.chat.yml

DOCKER_COMPOSE_CMD := docker compose


# Запуск всех микросервисов
up: up-users up-video up-likes up-comment up-chat

# Запуск микросервиса users
up-users:
	$(DOCKER_COMPOSE_CMD) -f $(USERS_COMPOSE_FILE) up --build -d

# Запуск микросервиса video
up-video:
	$(DOCKER_COMPOSE_CMD) -f $(VIDEO_COMPOSE_FILE) up --build -d

# Запуск микросервиса likes
up-likes:
	$(DOCKER_COMPOSE_CMD) -f $(LIKES_COMPOSE_FILE) up --build -d

# Запуск микросервиса comment
up-comment:
	$(DOCKER_COMPOSE_CMD) -f $(COMMENT_COMPOSE_FILE) up --build -d

# Запуск микросервиса chat
up-chat:
	$(DOCKER_COMPOSE_CMD) -f $(CHAT_COMPOSE_FILE) up --build -d


# Остановка всех микросервисов
stop: stop-users stop-video stop-likes stop-comment stop-chat

# Остановка микросервиса likes
stop-likes:
	$(DOCKER_COMPOSE_CMD) -f $(LIKES_COMPOSE_FILE) stop

# Остановка микросервиса video
stop-video:
	$(DOCKER_COMPOSE_CMD) -f $(VIDEO_COMPOSE_FILE) stop

# Остановка микросервиса users
stop-users:
	$(DOCKER_COMPOSE_CMD) -f $(USERS_COMPOSE_FILE) stop

# Остановка микросервиса comment
stop-comment:
	$(DOCKER_COMPOSE_CMD) -f $(COMMENT_COMPOSE_FILE) stop

# Остановка микросервиса comment
stop-chat:
	$(DOCKER_COMPOSE_CMD) -f $(CHAT_COMPOSE_FILE) stop


# Остановка и удаление всех контейнеров
down: down-likes down-video down-users down-comment down-chat

# Остановка и удаление контейнера likes
down-likes:
	$(DOCKER_COMPOSE_CMD) -f $(LIKES_COMPOSE_FILE) down

# Остановка и удаление контейнера video
down-video:
	$(DOCKER_COMPOSE_CMD) -f $(VIDEO_COMPOSE_FILE) down

# Остановка и удаление контейнера users
down-users:
	$(DOCKER_COMPOSE_CMD) -f $(USERS_COMPOSE_FILE) down

# Остановка и удаление контейнера comment
down-comment:
	$(DOCKER_COMPOSE_CMD) -f $(COMMENT_COMPOSE_FILE) down

# Остановка и удаление контейнера chat
down-chat:
	$(DOCKER_COMPOSE_CMD) -f $(CHAT_COMPOSE_FILE) down


# Остановка и удаление всех контейнеров вместе с volumes
down-v: down-likes-v down-video-v down-users-v down-video-v down-chat-v

# Остановка и удаление контейнера likes вместе с volumes
down-likes-v:
	$(DOCKER_COMPOSE_CMD) -f $(LIKES_COMPOSE_FILE) down -v

# Остановка и удаление контейнера video вместе с volumes
down-video-v:
	$(DOCKER_COMPOSE_CMD) -f $(VIDEO_COMPOSE_FILE) down -v

# Остановка и удаление контейнера users вместе с volumes
down-users-v:
	$(DOCKER_COMPOSE_CMD) -f $(USERS_COMPOSE_FILE) down -v

# Остановка и удаление контейнера comment вместе с volumes
down-comment-v:
	$(DOCKER_COMPOSE_CMD) -f $(COMMENT_COMPOSE_FILE) down -v

# Остановка и удаление контейнера chat вместе с volumes
down-chat-v:
	$(DOCKER_COMPOSE_CMD) -f $(CHAT_COMPOSE_FILE) down -v


# Создание миграций
migrate-video:
	$(DOCKER_COMPOSE_CMD) -f $(VIDEO_COMPOSE_FILE) exec app_video alembic revision --autogenerate -m $(commit)
migrate-likes:
	$(DOCKER_COMPOSE_CMD) -f $(LIKES_COMPOSE_FILE) exec app_likes alembic revision --autogenerate -m $(commit)
migrate-users:
	$(DOCKER_COMPOSE_CMD) -f $(USERS_COMPOSE_FILE) exec app_users alembic revision --autogenerate -m $(commit)
migrate-comment:
	$(DOCKER_COMPOSE_CMD) -f $(COMMENT_COMPOSE_FILE) exec app_comment alembic revision --autogenerate -m $(commit)
migrate-chat:
	$(DOCKER_COMPOSE_CMD) -f $(CHAT_COMPOSE_FILE) exec app_chat alembic revision --autogenerate -m $(commit)

# Создание сети
network:
	docker network create dev-youtube
# Удаление сети
network-delete:
	docker network rm dev-youtube
