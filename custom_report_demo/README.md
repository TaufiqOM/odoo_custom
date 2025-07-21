# Custom Report Demo Module

This module demonstrates how to create custom reports in Odoo 18, following the same pattern used in the `om_sale_blanket_order_it` module.

## Module Structure

```
custom_report_demo/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── custom_demo.py
├── reports/
│   ├── __init__.py
│   ├── custom_report_actions.xml
│   └── custom_report_template.xml
├── security/
│   └── ir.model.access.csv
├── views/
│   └── custom_demo_views.xml
├── data/
│   └── demo_data.xml
└── README.md
```

## Key Components

### 1. Report Definition (`reports/custom_report_actions.xml`)
- Defines the report action using `ir.actions.report`
- Links the report to the model (`custom.demo`)
- Sets the report type to PDF (`qweb-pdf`)

### 2. Report Template (`reports/custom_report_template.xml`)
- Uses QWeb templates for PDF generation
- Follows the same pattern as `om_sale_blanket_order_it`:
  - Uses `web.html_container` and `web.external_layout`
  - Includes responsive table design
  - Uses Odoo's built-in styling classes

### 3. Model Definition (`models/custom_demo.py`)
- Simple model with header and line items
- Includes computed fields for totals
- Uses standard Odoo ORM patterns

## Installation

1. Copy the `custom_report_demo` folder to your Odoo custom addons directory
2. Update the addons list in Odoo (Apps → Update Apps List)
3. Search for "Custom Report Demo" and install it

## Usage

1. Go to **Custom Demo → Custom Demo**
2. Create a new record or use the demo data
3. Click **Print → Custom Demo Report** to generate the PDF report

## Report Structure Analysis

Based on studying `om_sale_blanket_order_it`, the key patterns for creating reports are:

### 1. Report Registration
```xml
<record id="action_report_name" model="ir.actions.report">
    <field name="name">Report Name</field>
    <field name="model">your.model</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">module_name.report_template_name</field>
    <field name="report_file">module_name.report_template_name</field>
    <field name="binding_model_id" ref="model_your_model"/>
</record>
```

### 2. Template Structure
```xml
<template id="report_template_name">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="o">
            <t t-call="web.external_layout">
                <div class="page">
                    <!-- Your report content here -->
                </div>
            </t>
        </t>
    </t>
</template>
```

### 3. Data Access
- Use `t-field` for model fields
- Use `t-foreach` for iterating over records
- Use `t-options` for formatting (monetary, dates, etc.)

## Customization

To create your own report based on this template:

1. **Change the model**: Update the model name in all files
2. **Modify the template**: Edit the QWeb template in `custom_report_template.xml`
3. **Update fields**: Change the fields displayed in the report
4. **Add styling**: Use Bootstrap classes for responsive design
5. **Add new data**: Create new demo data in `data/demo_data.xml`

## Demo Data

The module includes demo data with:
- 2 sample customers (ABC Corporation, XYZ Industries)
- 3 sample products
- 2 sample reports with line items

## Technical Notes

- Uses Odoo 18's QWeb engine for PDF generation
- Supports responsive design with Bootstrap classes
- Includes proper access rights configuration
- Follows Odoo's standard module structure

## Troubleshooting

- If the report doesn't appear, check that all XML files are properly loaded in `__manifest__.py`
- Ensure the `ir.model.access.csv` has correct permissions
- Check Odoo logs for any QWeb template errors
