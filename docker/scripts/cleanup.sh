#!/bin/bash
# Cleanup script for Open Ear Trainer Docker resources

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
FORCE=false
ALL=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--force)
            FORCE=true
            shift
            ;;
        -a|--all)
            ALL=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  -f, --force    Force cleanup without confirmation"
            echo "  -a, --all      Clean up everything (images, volumes, networks)"
            echo "  -h, --help     Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0             # Clean up containers and volumes"
            echo "  $0 -a          # Clean up everything including images"
            echo "  $0 -f          # Force cleanup without confirmation"
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}🧹 Open Ear Trainer Docker Cleanup${NC}"
echo

# Change to docker directory
cd "$(dirname "$0")/.."

# Function to confirm action
confirm() {
    if [ "$FORCE" = true ]; then
        return 0
    fi

    read -p "$1 (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        return 0
    else
        return 1
    fi
}

# Stop and remove containers
echo -e "${BLUE}Stopping and removing containers...${NC}"
if confirm "Stop all Open Ear Trainer containers?"; then
    docker-compose -f docker-compose.yml down 2>/dev/null || true
    docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
    echo -e "${GREEN}✅ Containers stopped and removed${NC}"
fi

# Remove volumes
echo -e "${BLUE}Removing volumes...${NC}"
if confirm "Remove all Open Ear Trainer volumes?"; then
    docker volume ls -q | grep -E "(open-ear-trainer|logs|redis_data)" | xargs -r docker volume rm
    echo -e "${GREEN}✅ Volumes removed${NC}"
fi

# Remove images if --all flag is used
if [ "$ALL" = true ]; then
    echo -e "${BLUE}Removing images...${NC}"
    if confirm "Remove all Open Ear Trainer images?"; then
        docker images | grep -E "(open-ear-trainer|open_ear_trainer)" | awk '{print $3}' | xargs -r docker rmi -f
        echo -e "${GREEN}✅ Images removed${NC}"
    fi
fi

# Remove unused networks
echo -e "${BLUE}Removing unused networks...${NC}"
if confirm "Remove unused Docker networks?"; then
    docker network prune -f
    echo -e "${GREEN}✅ Unused networks removed${NC}"
fi

# Remove unused images (dangling)
echo -e "${BLUE}Removing dangling images...${NC}"
if confirm "Remove dangling images?"; then
    docker image prune -f
    echo -e "${GREEN}✅ Dangling images removed${NC}"
fi

# Remove unused volumes
echo -e "${BLUE}Removing unused volumes...${NC}"
if confirm "Remove unused volumes?"; then
    docker volume prune -f
    echo -e "${GREEN}✅ Unused volumes removed${NC}"
fi

echo -e "${GREEN}🎉 Cleanup completed successfully!${NC}"
echo -e "${YELLOW}Note: You may need to rebuild images and volumes for your next deployment.${NC}"
