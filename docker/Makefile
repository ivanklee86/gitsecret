SHELL := /bin/bash
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = envadmin-build

#-----------------------------------------------------------------------
# Rules of Rules : Grouped rules that _doathing_
#-----------------------------------------------------------------------



#-----------------------------------------------------------------------
# Run Rules
#-----------------------------------------------------------------------

# Run service in Docker for local testing
run:
	docker run -it --name ${PROJECT_NAME} --rm  ${PROJECT_NAME}:latest

#-----------------------------------------------------------------------
# Docker Rules
#-----------------------------------------------------------------------
# Build Docker container
build:
	docker build -t ${PROJECT_NAME} .

# Deletes stopped containers, unused volumes, and unused networks.
clean-docker:
	docker system prune -a
