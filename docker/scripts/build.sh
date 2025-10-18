#!/bin/bash
# Build script for Open Ear Trainer Docker images

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
ENVIRONMENT="prod"
TAG="open-ear-trainer"
PUSH=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -t|--tag)
            TAG="$2"
            shift 2
            ;;
        -p|--push)
            PUSH=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  -e, --env ENV     Environment (dev|prod) [default: prod]"
            echo "  -t, --tag TAG     Docker image tag [default: open-ear-trainer]"
            echo "  -p, --push        Push image to registry"
            echo "  -h, --help        Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}🐳 Building Open Ear Trainer Docker image${NC}"
echo -e "Environment: ${YELLOW}$ENVIRONMENT${NC}"
echo -e "Tag: ${YELLOW}$TAG${NC}"
echo -e "Push: ${YELLOW}$PUSH${NC}"
echo

# Change to project root
cd "$(dirname "$0")/../.."

# Build the image
echo -e "${GREEN}Building Docker image...${NC}"
docker build -f docker/Dockerfile -t "$TAG" .

if [ "$PUSH" = true ]; then
    echo -e "${GREEN}Pushing image to registry...${NC}"
    docker push "$TAG"
fi

echo -e "${GREEN}✅ Build completed successfully!${NC}"
echo -e "Image: ${YELLOW}$TAG${NC}"
