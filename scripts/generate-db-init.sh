#!/bin/bash

# Script to generate SQL init files from templates using environment variables
# This ensures database users are created with the correct passwords from .env

set -e

# Source the .env file to get environment variables
if [ -f .env ]; then
    set -a
    source .env
    set +a
else
    echo "Error: .env file not found"
    exit 1
fi

echo "🔧 Generating database init files from templates..."

# Function to replace placeholders in template files
process_template() {
    local template_file="$1"
    local output_file="$2"
    
    if [ ! -f "$template_file" ]; then
        echo "Error: Template file $template_file not found"
        exit 1
    fi
    
    echo "Processing $template_file -> $output_file"
    
    # Use sed to replace {{VAR}} with actual values
    sed \
        -e "s/{{POSTGRES_HYDRA_DB}}/${POSTGRES_HYDRA_DB}/g" \
        -e "s/{{POSTGRES_HYDRA_USER}}/${POSTGRES_HYDRA_USER}/g" \
        -e "s/{{POSTGRES_HYDRA_PASSWORD}}/${POSTGRES_HYDRA_PASSWORD}/g" \
        -e "s/{{POSTGRES_AUTH_DB}}/${POSTGRES_AUTH_DB}/g" \
        -e "s/{{POSTGRES_AUTH_USER}}/${POSTGRES_AUTH_USER}/g" \
        -e "s/{{POSTGRES_AUTH_PASSWORD}}/${POSTGRES_AUTH_PASSWORD}/g" \
        "$template_file" > "$output_file"
    
    echo "✅ Generated $output_file"
}

# Process Hydra init.sql template
process_template "database/hydra/init.sql.template" "database/hydra/init.sql"

# Process Auth init.sql template  
process_template "database/auth/init.sql.template" "database/auth/init.sql"

echo "🎉 All database init files generated successfully!"
echo ""
echo "Generated files:"
echo "  - database/hydra/init.sql"
echo "  - database/auth/init.sql"
echo ""
echo "These files are now ready for use with docker-compose."
