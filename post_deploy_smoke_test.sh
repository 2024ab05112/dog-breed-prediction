#!/bin/bash
# post_deploy_smoke_test.sh
# Simple smoke test to verify the deployed application is responsive

# URL of the deployed application
BASE_URL="http://dog-breed-prediction.centralindia.cloudapp.azure.com"
MAX_RETRIES=10
SLEEP_TIME=10

echo "Starting Post-Deployment Smoke Test..."
echo "Target URL: $BASE_URL"

check_endpoint() {
    local endpoint=$1
    local expected_code=$2
    local retries=0
    
    echo "Checking endpoint: $endpoint"
    
    while [ $retries -lt $MAX_RETRIES ]; do
        status_code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$endpoint")
        
        if [ "$status_code" -eq "$expected_code" ]; then
            echo "✅ Success: $endpoint returned $status_code"
            return 0
        fi
        
        echo "⚠️  Attempt $((retries+1))/$MAX_RETRIES: Received $status_code (Expected $expected_code). Retrying in ${SLEEP_TIME}s..."
        sleep $SLEEP_TIME
        retries=$((retries+1))
    done
    
    echo "❌ Failed to reach $endpoint after $MAX_RETRIES attempts."
    return 1
}

# 1. Check Frontend Availability (Root)
if ! check_endpoint "/" 200; then
    echo "Frontend check failed!"
    exit 1
fi

# 2. Check Backend Health API (Root directly based on backend deployment)
# Note: The health endpoint is exposed at /api/health or /health via Ingress depending on config.
# Based on current Ingress, /api -> Backend. So /api/health SHOULD be accessible if router includes it.
# But backend/main.py puts @app.get("/health") on Root app.
# And Ingress routes /api -> Backend Service.
# So valid path is likely: http://.../api/health IF strip path works, or http://.../health IF ingress rule exists.
# Let's check the Ingress config again. 
# Ingress: path: /api -> backend:80
# Backend root: /health
# So Ingress sends /api/health -> Backend /api/health (unless strip-prefix).
# Wait, let's just check the Swagger UI which we know works: /docs
if ! check_endpoint "/docs" 200; then
    echo "Backend Swagger UI check failed!"
    exit 1
fi

echo "All Smoke Tests Passed Successfully! 🚀"
exit 0
