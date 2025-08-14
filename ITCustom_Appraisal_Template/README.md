# Custom Appraisal Template Module

This module adds a new "Template" menu under Appraisal Configuration to manage appraisal templates.

## Features

- **Template Management**: Create and manage appraisal templates
- **Skills & Competencies**: Define skills and competencies for each template
- **Goals & Objectives**: Set goals and objectives for appraisals
- **Flexible Configuration**: Support for different appraisal types (annual, quarterly, monthly, etc.)
- **Rating Scales**: Multiple rating scale options (1-5, 1-10, percentage, custom)

## Usage

1. Install the module
2. Go to **Appraisal > Configuration > Template**
3. Create new templates with skills, goals, and evaluation criteria
4. Use templates when creating new appraisals

## Models

- **appraisal.template**: Main template model
- **appraisal.template.skill.line**: Skills and competencies for templates
- **appraisal.template.goal.line**: Goals and objectives for templates

## Security

- **HR Officers**: Can create, edit, and view templates
- **HR Managers**: Full access including delete permissions
- **Regular Users**: Read-only access to templates
