from odoo import models, fields, api

class PerformanceGuidelinesWizard(models.TransientModel):
    _name = 'performance.guidelines.wizard'
    _description = 'Performance Guidelines Wizard'
    
    appraisal_id = fields.Many2one('hr.appraisal', string='Appraisal', required=True)
    performance_guidelines_umum_html = fields.Html(
        string="Pedoman Penilaian Kerja Umum",
        compute="_compute_guidelines_html"
    )
    performance_guidelines_khusus_html = fields.Html(
        string="Pedoman Penilaian Kerja Khusus",
        compute="_compute_guidelines_html"
    )
    performance_guidelines_kepemimpinan_html = fields.Html(
        string="Pedoman Penilaian Kepemimpinan",
        compute="_compute_guidelines_html"
    )
    
    @api.depends('appraisal_id')
    def _compute_guidelines_html(self):
        for wizard in self:
            if wizard.appraisal_id and wizard.appraisal_id.department_id:
                # Find appraisal templates that match the department_id
                matching_templates = self.env['appraisal.template'].search([
                    ('department_id', '=', wizard.appraisal_id.department_id.id)
                ])
                
                # Collect umum guidelines
                umum_guidelines = []
                for template in matching_templates:
                    umum_guidelines.extend(template.performance_guidelines_umum)
                
                # Collect khusus guidelines
                khusus_guidelines = []
                for template in matching_templates:
                    khusus_guidelines.extend(template.performance_guidelines_khusus)
                
                # Collect kepemimpinan guidelines (only if has subordinates)
                kepemimpinan_guidelines = []
                if wizard.appraisal_id.memiliki_bawahan:
                    for template in matching_templates:
                        kepemimpinan_guidelines.extend(template.performance_guidelines_kepemimpinan)
                
                # Generate HTML for Umum guidelines
                if umum_guidelines:
                    umum_html = self._generate_guidelines_html(umum_guidelines, "Umum")
                    wizard.performance_guidelines_umum_html = umum_html
                else:
                    wizard.performance_guidelines_umum_html = False
                
                # Generate HTML for Khusus guidelines
                if khusus_guidelines:
                    khusus_html = self._generate_guidelines_html(khusus_guidelines, "Khusus")
                    wizard.performance_guidelines_khusus_html = khusus_html
                else:
                    wizard.performance_guidelines_khusus_html = False
                
                # Generate HTML for Kepemimpinan guidelines (only if has subordinates)
                if kepemimpinan_guidelines:
                    kepemimpinan_html = self._generate_guidelines_html(kepemimpinan_guidelines, "Kepemimpinan")
                    wizard.performance_guidelines_kepemimpinan_html = kepemimpinan_html
                else:
                    wizard.performance_guidelines_kepemimpinan_html = False
            else:
                wizard.performance_guidelines_umum_html = False
                wizard.performance_guidelines_khusus_html = False
                wizard.performance_guidelines_kepemimpinan_html = False
    
    def _generate_guidelines_html(self, guidelines, type_name):
        """Helper method to generate HTML for guidelines"""
        if not guidelines:
            return False
            
        html_content = f"""
        <style>
            .performance-guidelines-table-{type_name.lower()} {{
                width: 100%;
                border-collapse: collapse;
                border: 2px solid #444;
                font-size: 12px;
            }}
            .performance-guidelines-table-{type_name.lower()} th, 
            .performance-guidelines-table-{type_name.lower()} td {{
                border: 1px solid #444;
                padding: 6px;
                text-align: left;
                vertical-align: top;
            }}
            .performance-guidelines-table-{type_name.lower()} th {{
                background-color: #f2f2f2;
                font-weight: bold;
                font-size: 11px;
            }}
            .performance-guidelines-table-{type_name.lower()} tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .guidelines-header {{
                background-color: #e8f4f8;
                padding: 10px;
                margin-bottom: 15px;
                border-left: 4px solid #007bff;
            }}
        </style>
        <div class="guidelines-header">
            <h4>Pedoman Penilaian Kerja {type_name}</h4>
        </div>
        <table class="performance-guidelines-table-{type_name.lower()}">
            <thead>
                <tr>
                    <th>Faktor Perilaku Kerja</th>
                    <th>Definisi</th>
                    <th>NILAI 1<br/>(Kurang Diterima)</th>
                    <th>NILAI 2<br/>(Butuh Arahan)</th>
                    <th>NILAI 3<br/>(Standart)</th>
                    <th>NILAI 4<br/>(Performa Bagus)</th>
                    <th>NILAI 5<br/>(Luar Biasa)</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for guideline in guidelines:
            html_content += f"""
                <tr>
                    <td><strong>{guideline.factor or ''}</strong></td>
                    <td>{guideline.definition or ''}</td>
                    <td>{guideline.value_1 or ''}</td>
                    <td>{guideline.value_2 or ''}</td>
                    <td>{guideline.value_3 or ''}</td>
                    <td>{guideline.value_4 or ''}</td>
                    <td>{guideline.value_5 or ''}</td>
                </tr>
            """
        
        html_content += """
            </tbody>
        </table>
        """
        return html_content
    
    def action_close(self):
        """Close the wizard"""
        return {'type': 'ir.actions.act_window_close'}
