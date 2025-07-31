#!/bin/bash

# Generate JWT signing keys for the auth backend
# This script creates RSA key pairs for JWT signing

set -e

# Create keys directory if it doesn't exist
mkdir -p keys

# Generate private key
openssl genrsa -out keys/jwt_private.pem 2048

# Generate public key from private key
openssl rsa -in keys/jwt_private.pem -pubout -out keys/jwt_public.pem

# Set proper permissions
chmod 600 keys/jwt_private.pem
chmod 644 keys/jwt_public.pem

echo "JWT signing keys generated successfully:"
echo "  Private key: keys/jwt_private.pem"
echo "  Public key: keys/jwt_public.pem"
echo ""
echo "Make sure to keep the private key secure and never commit it to version control."
