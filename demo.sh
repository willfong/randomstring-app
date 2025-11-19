#!/bin/bash

# Demo script to show the new smart root endpoint behavior

echo "=================================================="
echo "RandomString API - Smart Root Endpoint Demo"
echo "=================================================="
echo ""

echo "1. Testing with curl (API client - should get plain text):"
echo "   $ curl http://localhost:8000/"
echo ""
curl -s http://localhost:8000/
echo ""

echo "=================================================="
echo ""
echo "2. Testing with browser User-Agent (should redirect to /docs):"
echo "   $ curl -H 'User-Agent: Mozilla/5.0 Chrome/91.0' http://localhost:8000/"
echo ""
curl -s -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0" \
     -w "Status: %{http_code}\nRedirect: %{redirect_url}\n" \
     http://localhost:8000/
echo ""

echo "=================================================="
echo ""
echo "3. Testing custom length endpoint (backward compatible):"
echo "   $ curl http://localhost:8000/16"
echo ""
curl -s http://localhost:8000/16
echo ""

echo "=================================================="
echo ""
echo "4. Testing new JSON API endpoint:"
echo "   $ curl http://localhost:8000/api/v1/random?length=8"
echo ""
curl -s http://localhost:8000/api/v1/random?length=8 | python3 -m json.tool
echo ""

echo "=================================================="
echo "Demo complete!"
echo "=================================================="
