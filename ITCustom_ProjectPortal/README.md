# ITCustom_ProjectPortal

## Overview

This Odoo module extends the default project functionality to allow portal users to be assigned to project tasks, in addition to internal users.

## Features

- **Extended Assignee Selection**: By default, Odoo restricts task assignees to internal users only. This module removes that restriction, allowing both internal and portal users to be assigned to tasks.
- **Seamless Integration**: The module inherits from the core `project.task` model and modifies the `user_ids` field domain to include portal users.
- **Backward Compatibility**: The module maintains compatibility with existing Odoo installations and does not affect other functionality.

## Technical Details

### Model Inheritance

The module inherits from `project.task` and overrides the `user_ids` field:

```python
class ProjectTask(models.Model):
    _inherit = 'project.task'

    user_ids = fields.Many2many(
        'res.users',
        relation='project_task_user_rel',
        column1='task_id',
        column2='user_id',
        string='Assignees',
        context={'active_test': False},
        tracking=True,
        domain="[('active', '=', True)]"  # Allows both internal and portal users
    )
```

### Dependencies

- `project`: Core project management module
- `portal`: Portal functionality for external users

## Installation

1. Place the module in your Odoo addons directory
2. Update your Odoo configuration to include the custom addons path
3. Install the module through the Odoo Apps menu or using the command line

## Usage

After installation:

1. Create or edit a project task
2. In the "Assignees" field, you can now select both internal users and portal users
3. Portal users will receive notifications and can view assigned tasks through the portal interface

## Testing

To test the functionality:

1. Create a portal user
2. Create a project task
3. Verify that the portal user appears in the assignee selection dropdown
4. Assign the task to the portal user
5. Check that the portal user can access the task through the portal

## Compatibility

- Compatible with Odoo versions that support the project and portal modules
- Tested with standard Odoo project workflows
- May require additional configuration for custom project setups

## Support

For support or questions about this module, please contact the ITCustom development team.
