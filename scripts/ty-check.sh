#!/bin/bash
# Ty type checking wrapper for pre-commit hooks
# This script runs Ty and fails the commit on type errors

echo "🔍 Running Ty type checking..."
uv run ty check backend/

# Return the exit code from Ty (0 = success, non-zero = errors)
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "✅ Ty check passed!"
else
    echo "❌ Ty check failed with $exit_code errors"
    echo "💡 Fix the type errors above or configure exceptions in pyproject.toml"
fi

exit $exit_code
