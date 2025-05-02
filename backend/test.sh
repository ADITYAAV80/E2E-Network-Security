#!/bin/bash

BASE_URL="http://192.168.49.2.nip.io/api"

echo "🧪 Testing /login"
hey -n 500 -c 20 -m POST -H "Content-Type: application/json" \
-d '{"email":"customer@gmail.com","password":"test123"}' \
"$BASE_URL/login"

echo "🧪 Testing /signup"
hey -n 300 -c 10 -m POST -H "Content-Type: application/json" \
-d '{"email":"newuser@gmail.com","password":"test123", "username": "newuser"}' \
"$BASE_URL/signup"
