#!/bin/bash
# Deployment script for Open Ear Trainer

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
ENVIRONMENT="prod"
ACTION="up"
DETACHED=true

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -a|--action)
            ACTION="$2"
            shift 2
            ;;
        -d|--detached)
            DETACHED=true
            shift
            ;;
        -f|--foreground)
            DETACHED=false
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  -e, --env ENV       Environment (dev|prod) [default: prod]"
            echo "  -a, --action ACTION Action (up|down|restart|logs) [default: up]"
            echo "  -d, --detached      Run in detached mode [default]"
            echo "  -f, --foreground    Run in foreground mode"
            echo "  -h, --help          Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 -e dev -a up     # Start development environment"
            echo "  $0 -e prod -a up    # Start production environment"
            echo "  $0 -a down          # Stop all services"
            echo "  $0 -a logs          # Show logs"
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}🚀 Open Ear Trainer Deployment${NC}"
echo -e "Environment: ${YELLOW}$ENVIRONMENT${NC}"
echo -e "Action: ${YELLOW}$ACTION${NC}"
echo -e "Mode: ${YELLOW}$([ "$DETACHED" = true ] && echo "detached" || echo "foreground")${NC}"
echo

# Change to docker directory
cd "$(dirname "$0")/.."

# Set compose file based on environment
COMPOSE_FILE="docker-compose.yml"
if [ "$ENVIRONMENT" = "dev" ]; then
    COMPOSE_FILE="docker-compose.dev.yml"
elif [ "$ENVIRONMENT" = "prod" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
fi

# Check if compose file exists
if [ ! -f "$COMPOSE_FILE" ]; then
    echo -e "${RED}❌ Compose file $COMPOSE_FILE not found!${NC}"
    exit 1
fi

# Execute action
case $ACTION in
    up)
        echo -e "${BLUE}Starting services...${NC}"
        if [ "$DETACHED" = true ]; then
            docker-compose -f "$COMPOSE_FILE" up -d
        else
            docker-compose -f "$COMPOSE_FILE" up
        fi
        ;;
    down)
        echo -e "${BLUE}Stopping services...${NC}"
        docker-compose -f "$COMPOSE_FILE" down
        ;;
    restart)
        echo -e "${BLUE}Restarting services...${NC}"
        docker-compose -f "$COMPOSE_FILE" restart
        ;;
    logs)
        echo -e "${BLUE}Showing logs...${NC}"
        docker-compose -f "$COMPOSE_FILE" logs -f
        ;;
    build)
        echo -e "${BLUE}Building services...${NC}"
        docker-compose -f "$COMPOSE_FILE" build
        ;;
    *)
        echo -e "${RED}❌ Unknown action: $ACTION${NC}"
        echo "Available actions: up, down, restart, logs, build"
        exit 1
        ;;
esac

echo -e "${GREEN}✅ Action completed successfully!${NC}"

# Show status if action was up
if [ "$ACTION" = "up" ] && [ "$DETACHED" = true ]; then
    echo -e "${BLUE}Service status:${NC}"
    docker-compose -f "$COMPOSE_FILE" ps
fi
