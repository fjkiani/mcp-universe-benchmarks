#!/bin/bash
# Script to create pyproject.toml for each server

SERVERS=(
  "weather:Weather data and forecasts:mcp,requests,python-dotenv"
  "wikipedia:Wikipedia article search:mcp,wikipedia-api,python-dotenv"
  "yahoo_finance:Stock market data:mcp,yfinance,python-dotenv"
  "currency_converter:Currency conversion:mcp,requests,python-dotenv"
  "calendar:Calendar and scheduling:mcp,python-dotenv"
  "date:Date and time utilities:mcp,python-dotenv"
  "echo:Echo server for testing:mcp,python-dotenv"
  "email:Email functionality:mcp,python-dotenv"
  "file_storage:File storage management:mcp,python-dotenv"
  "task_management:Task tracking:mcp,python-dotenv"
  "url_shortener:URL shortening:mcp,requests,python-dotenv"
  "pdf_generator:PDF generation:mcp,reportlab,python-dotenv"
  "image_processing:Image manipulation:mcp,PIL,python-dotenv"
  "blender:Blender 3D integration:mcp,blender-mcp,python-dotenv"
  "google_sheets:Google Sheets integration:mcp,google-api-python-client,google-auth,python-dotenv"
  "stripe_payments:Stripe payments:mcp,stripe,python-dotenv"
  "sms_messaging:SMS via Twilio:mcp,twilio,python-dotenv"
  "invoicing:Invoice management:mcp,python-dotenv"
  "subscription_management:Subscription billing:mcp,python-dotenv"
  "stock_portfolio:Portfolio management:mcp,python-dotenv"
  "crypto_intelligence:Cryptocurrency data:mcp,requests,python-dotenv"
  "api_football:Football data API:mcp,requests,python-dotenv"
  "flight_delay:Flight delay info:mcp,requests,python-dotenv"
  "receptionist_sim:Receptionist simulation:mcp,python-dotenv"
  "it_support_desk:IT support tickets:mcp,python-dotenv"
)

for server_info in "${SERVERS[@]}"; do
  IFS=':' read -r name desc deps <<< "$server_info"
  
  if [ -d "$name" ]; then
    echo "Creating pyproject.toml for $name"
    
    # Convert deps to formatted list
    dep_list=""
    IFS=',' read -ra DEP_ARRAY <<< "$deps"
    for dep in "${DEP_ARRAY[@]}"; do
      case $dep in
        mcp) dep_list="$dep_list    \"mcp>=1.9.4\",\n" ;;
        requests) dep_list="$dep_list    \"requests>=2.32.0\",\n" ;;
        python-dotenv) dep_list="$dep_list    \"python-dotenv>=1.0.0\",\n" ;;
        *) dep_list="$dep_list    \"$dep\",\n" ;;
      esac
    done
    
    # Remove trailing comma and newline
    dep_list=$(echo -e "$dep_list" | sed '$ s/,$//')
    
    cat > "$name/pyproject.toml" << PYPROJECT
[project]
name = "lbx-mcp-${name//_/-}"
version = "1.0.0"
description = "${desc}"
readme = "README.md"
requires-python = ">=3.12"
authors = [
    { name = "LBX MCP Team" }
]
dependencies = [
$(echo -e "$dep_list")
]

[project.scripts]
${name//_/-}-server = "${name}.server:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["${name}"]
PYPROJECT
  fi
done

echo "Done creating pyproject.toml files"
