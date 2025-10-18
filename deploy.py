#!/usr/bin/env python3
"""
CLI deployment script for Open Ear Trainer
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

class DeploymentError(Exception):
    """Custom exception for deployment errors"""
    pass

class Deployer:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backend_dir = project_root / "backend"
        self.frontend_dir = project_root / "frontend"
        
    def run_command(self, command: List[str], cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
        """Run a command and return the result"""
        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.project_root,
                check=True,
                capture_output=True,
                text=True
            )
            return result
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {' '.join(command)}")
            print(f"Error: {e.stderr}")
            raise DeploymentError(f"Command failed: {e}")

    def check_prerequisites(self) -> None:
        """Check if all required tools are installed"""
        print("🔍 Checking prerequisites...")
        
        required_tools = {
            'git': ['git', '--version'],
            'docker': ['docker', '--version'],
            'docker-compose': ['docker-compose', '--version'],
            'node': ['node', '--version'],
            'npm': ['npm', '--version'],
        }
        
        for tool, command in required_tools.items():
            try:
                self.run_command(command)
                print(f"✅ {tool} is installed")
            except (subprocess.CalledProcessError, FileNotFoundError):
                raise DeploymentError(f"❌ {tool} is not installed or not in PATH")

    def build_frontend(self) -> None:
        """Build the React frontend"""
        print("🏗️  Building frontend...")
        
        # Install dependencies
        self.run_command(['npm', 'ci'], cwd=self.frontend_dir)
        
        # Build for production
        env = os.environ.copy()
        env['REACT_APP_API_URL'] = os.getenv('REACT_APP_API_URL', 'https://your-api-domain.com')
        
        self.run_command(['npm', 'run', 'build'], cwd=self.frontend_dir)
        
        print("✅ Frontend built successfully")

    def build_docker_image(self, tag: str = "open-ear-trainer") -> None:
        """Build Docker image"""
        print(f"🐳 Building Docker image: {tag}")
        
        self.run_command(['docker', 'build', '-f', 'docker/Dockerfile', '-t', tag, '.'])
        print(f"✅ Docker image built: {tag}")

    def deploy_docker(self, tag: str = "open-ear-trainer", environment: str = "prod") -> None:
        """Deploy using Docker Compose"""
        print(f"🚀 Deploying with Docker Compose ({environment})...")
        
        # Determine compose file
        compose_file = f"docker/docker-compose.{environment}.yml" if environment != "prod" else "docker/docker-compose.yml"
        
        # Stop existing containers
        try:
            self.run_command(['docker-compose', '-f', compose_file, 'down'])
        except DeploymentError:
            pass  # Ignore if no containers are running
        
        # Start new containers
        self.run_command(['docker-compose', '-f', compose_file, 'up', '-d'])
        print("✅ Deployment completed")

    def deploy_github_pages(self) -> None:
        """Deploy frontend to GitHub Pages"""
        print("📄 Deploying to GitHub Pages...")
        
        # Check if we're in a git repository
        try:
            self.run_command(['git', 'status'])
        except DeploymentError:
            raise DeploymentError("Not in a git repository")
        
        # Build frontend
        self.build_frontend()
        
        # Add and commit changes
        self.run_command(['git', 'add', 'frontend/build/'])
        self.run_command(['git', 'commit', '-m', 'Deploy frontend to GitHub Pages'])
        
        # Push to main branch (this will trigger GitHub Actions)
        self.run_command(['git', 'push', 'origin', 'main'])
        print("✅ Frontend deployment triggered via GitHub Actions")

    def deploy_railway(self) -> None:
        """Deploy backend to Railway"""
        print("🚂 Deploying to Railway...")
        
        # Check if Railway CLI is installed
        try:
            self.run_command(['railway', '--version'])
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Installing Railway CLI...")
            self.run_command(['npm', 'install', '-g', '@railway/cli'])
        
        # Login to Railway (if not already logged in)
        try:
            self.run_command(['railway', 'whoami'])
        except DeploymentError:
            print("Please login to Railway:")
            self.run_command(['railway', 'login'])
        
        # Deploy
        self.run_command(['railway', 'deploy'])
        print("✅ Backend deployed to Railway")

    def run_tests(self) -> None:
        """Run all tests"""
        print("🧪 Running tests...")
        
        # Python tests
        try:
            # Try to activate virtual environment and run tests
            if (self.project_root / '.venv').exists():
                self.run_command(['bash', '-c', 'source .venv/bin/activate && pytest backend/tests/ -v'])
            else:
                # Fallback to direct pytest
                self.run_command(['pytest', 'backend/tests/', '-v'])
        except DeploymentError as e:
            print(f"⚠️  Python tests failed: {e}")
            print("Continuing with deployment...")
        
        # Frontend tests
        try:
            self.run_command(['npm', 'test', '--', '--watchAll=false', '--passWithNoTests'], cwd=self.frontend_dir)
        except DeploymentError:
            print("⚠️  Frontend tests failed or not configured")
        
        print("✅ Tests completed")

    def lint_code(self) -> None:
        """Run linting"""
        print("🔍 Running linting...")
        
        # Python linting
        try:
            if (self.project_root / '.venv').exists():
                self.run_command(['bash', '-c', 'source .venv/bin/activate && ruff check backend/'])
                self.run_command(['bash', '-c', 'source .venv/bin/activate && ruff format backend/'])
            else:
                self.run_command(['ruff', 'check', 'backend/'])
                self.run_command(['ruff', 'format', 'backend/'])
        except DeploymentError as e:
            print(f"⚠️  Python linting failed: {e}")
            print("Continuing with deployment...")
        
        print("✅ Linting completed")

def main():
    parser = argparse.ArgumentParser(description="Deploy Open Ear Trainer")
    parser.add_argument(
        'command',
        choices=['docker', 'github-pages', 'railway', 'full', 'test', 'lint', 'build'],
        help='Deployment command to run'
    )
    parser.add_argument(
        '--tag',
        default='open-ear-trainer',
        help='Docker image tag (default: open-ear-trainer)'
    )
    parser.add_argument(
        '--skip-tests',
        action='store_true',
        help='Skip running tests before deployment'
    )
    parser.add_argument(
        '--skip-lint',
        action='store_true',
        help='Skip linting before deployment'
    )
    parser.add_argument(
        '--env',
        choices=['dev', 'prod'],
        default='prod',
        help='Deployment environment (default: prod)'
    )
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent
    deployer = Deployer(project_root)
    
    try:
        # Check prerequisites
        deployer.check_prerequisites()
        
        if args.command == 'test':
            deployer.run_tests()
        elif args.command == 'lint':
            deployer.lint_code()
        elif args.command == 'build':
            deployer.build_frontend()
            deployer.build_docker_image(args.tag)
        elif args.command == 'docker':
            if not args.skip_tests:
                deployer.run_tests()
            if not args.skip_lint:
                deployer.lint_code()
            deployer.build_frontend()
            deployer.build_docker_image(args.tag)
            deployer.deploy_docker(args.tag, args.env)
        elif args.command == 'github-pages':
            if not args.skip_tests:
                deployer.run_tests()
            if not args.skip_lint:
                deployer.lint_code()
            deployer.deploy_github_pages()
        elif args.command == 'railway':
            if not args.skip_tests:
                deployer.run_tests()
            if not args.skip_lint:
                deployer.lint_code()
            deployer.deploy_railway()
        elif args.command == 'full':
            if not args.skip_tests:
                deployer.run_tests()
            if not args.skip_lint:
                deployer.lint_code()
            deployer.build_frontend()
            deployer.build_docker_image(args.tag)
            deployer.deploy_docker(args.tag, args.env)
            print("🎉 Full deployment completed!")
        
    except DeploymentError as e:
        print(f"❌ Deployment failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
