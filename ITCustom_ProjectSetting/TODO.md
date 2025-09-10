# TODO for ITCustom_ProjectSetting Module

## Completed Tasks
- [x] Updated __manifest__.py to include views and wizard files (fixed data loading issue)
- [x] Created views/project_views.xml to inherit project form and kanban views, updating visibility conditions for "Share Project" button/menu to include 'invited_only'
- [x] Updated models/project.py to override action_open_share_project_wizard and _check_project_sharing_access methods to support 'invited_only' projects
- [x] Created wizard/project_share_wizard.py to override action_send_mail method to prevent changing privacy_visibility to 'portal' for 'invited_only' projects
- [x] Updated security/project_rules.xml to allow collaborators access to 'invited_only' projects
- [x] Updated models/project.py to allow access_token for 'invited_only' projects to enable public links

## Pending Tasks
- [ ] Test the module installation and functionality
- [ ] Verify that "Share Project" button appears for 'invited_only' projects
- [ ] Test sharing functionality for 'invited_only' projects
- [ ] Check for any edge cases or additional requirements

## Notes
- The module extends the project model to add 'invited_only' privacy visibility option
- Sharing wizard now supports 'invited_only' projects without changing their visibility
- Access control methods updated to allow sharing for 'invited_only' projects
