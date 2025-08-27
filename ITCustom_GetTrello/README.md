# ITCustom_GetTrello Module

## Overview
This module provides integration between Odoo and Trello, allowing synchronization of Trello boards, lists, and cards to Odoo Projects and Tasks.

## Features
- Trello API connection testing
- Full data synchronization from Trello to Odoo
- Automatic creation of projects from Trello lists
- Automatic creation of tasks from Trello cards
- Duplicate detection and prevention
- Real-time progress notifications
- Comprehensive error handling

## Installation
1. Install the module: `python odoo-bin -i ITCustom_GetTrello`
2. Go to Settings → General Settings → Trello Integration
3. Enable Trello integration
4. Provide your Trello API Key, API Token, and Board ID
5. Test the connection using the "Test Connection" button
6. Sync data using the "Sync Data" button

## Configuration
### Trello API Credentials
1. Go to https://trello.com/power-ups/admin
2. Create a new API key
3. Generate an API token
4. Copy both key and token to Odoo settings

### Trello Board ID
1. Open your Trello board in a web browser
