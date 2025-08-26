from odoo import models, fields, api

class PerformanceGuidelinesWizard(models.TransientModel):
    _name = 'performance.guidelines.wizard'
    _description = 'Performance Guidelines Wizard'
    
    appraisal_id = fields.Many2one('hr.appraisal', string='Appraisal', required=True)
    performance_guidelines_umum_html = fields.Html(
        string="Pedoman Penilaian Perilaku Kerja",
        compute="_compute_guidelines_html"
    )
    performance_guidelines_khusus_html = fields.Html(
        string="Pedoman Penilaian Hasil Kerja",
        compute="_compute_guidelines_html"
    )
    performance_guidelines_kepemimpinan_html = fields.Html(
        string="Pedoman Penilaian Kepemimpinan",
        compute="_compute_guidelines_html"
    )
    performance_guidelines_skill_html = fields.Html(
        string="Pedoman Penilaian Skill",
        compute="_compute_skill_guidelines_html"
    )
    
    @api.depends('appraisal_id')
    def _compute_guidelines_html(self):
        for wizard in self:
            if wizard.appraisal_id and wizard.appraisal_id.department_id:
                # Determine the correct template based on employee role
                is_atasan = wizard.appraisal_id.memiliki_bawahan
                
                # Find the specific template that matches department and role
                template = self.env['appraisal.template'].search([
                    ('department_id', '=', wizard.appraisal_id.department_id.id),
                    ('atasan', '=', is_atasan)
                ], limit=1)
                
                # If no specific template found, try without role filter
                if not template:
                    template = self.env['appraisal.template'].search([
                        ('department_id', '=', wizard.appraisal_id.department_id.id)
                    ], limit=1)
                
                # Collect guidelines from the specific template
                umum_guidelines = template.performance_guidelines_umum if template else []
                khusus_guidelines = template.performance_guidelines_khusus if template else []
                
                # Only collect kepemimpinan guidelines if employee is a manager/atasan
                kepemimpinan_guidelines = []
                if template and is_atasan:
                    kepemimpinan_guidelines = template.performance_guidelines_kepemimpinan
                
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
        
        # Determine the header based on type_name
        if type_name == "Umum":
            header_text = "Faktor Perilaku Kerja"
        elif type_name == "Khusus":
            header_text = "Hasil Kerja"
        else:  # Kepemimpinan
            header_text = "Faktor Perilaku Kerja"
            
        # Determine the display title based on type_name
        if type_name == "Umum":
            display_title = "Pedoman Penilaian Perilaku Kerja"
        elif type_name == "Khusus":
            display_title = "Pedoman Penilaian Hasil Kerja"
        else:  # Kepemimpinan
            display_title = "Pedoman Penilaian Kepemimpinan"
            
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
            <h4>{display_title}</h4>
        </div>
        <table class="performance-guidelines-table-{type_name.lower()}">
            <thead>
                <tr>
                    <th>{header_text}</th>
                    <th>Definisi</th>
                    <th>NILAI 20%<br/>(Kurang Diterima)</th>
                    <th>NILAI 40%<br/>(Butuh Arahan)</th>
                    <th>NILAI 60%<br/>(Standart)</th>
                    <th>NILAI 80%<br/>(Performa Bagus)</th>
                    <th>NILAI 100%<br/>(Luar Biasa)</th>
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
    
    @api.depends('appraisal_id')
    def _compute_skill_guidelines_html(self):
        """Compute HTML for skill guidelines grouped by skill type"""
        for wizard in self:
            if wizard.appraisal_id:
                # Get all skills for this appraisal
                appraisal_skills = self.env['hr.appraisal.skill'].search([
                    ('appraisal_id', '=', wizard.appraisal_id.id)
                ])
                
                # Group skills by skill type
                skills_by_type = {}
                for skill in appraisal_skills:
                    skill_type_name = skill.skill_type_id.name or 'Lainnya'
                    if skill_type_name not in skills_by_type:
                        skills_by_type[skill_type_name] = []
                    skills_by_type[skill_type_name].append(skill)
                
                # Generate HTML content
                html_content = self._generate_skill_guidelines_html(skills_by_type)
                wizard.performance_guidelines_skill_html = html_content
            else:
                wizard.performance_guidelines_skill_html = False
    
    def _generate_skill_guidelines_html(self, skills_by_type):
        """Generate HTML for skills grouped by type"""
        if not skills_by_type:
            return "<div style='padding: 20px; text-align: center; color: #999;'>Tidak ada data skill yang tersedia.</div>"
        
        html_content = """
        <style>
            .skill-guidelines-container {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                margin: 20px;
            }
            .skill-type-header {
                background-color: #007bff;
                color: white;
                padding: 12px 15px;
                margin: 25px 0 15px 0;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
            }
            .skill-list {
                list-style-type: none;
                padding: 0;
                margin: 0 0 30px 0;
            }
            .skill-item {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 5px;
                margin-bottom: 10px;
                padding: 15px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            .skill-item:hover {
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            }
            .skill-name {
                font-weight: 600;
                color: #212529;
                font-size: 15px;
                margin-bottom: 5px;
            }
            .skill-details {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                margin-top: 8px;
            }
            .skill-level {
                color: #6c757d;
                font-size: 14px;
                background-color: #f8f9fa;
                padding: 4px 8px;
                border-radius: 3px;
                border: 1px solid #e9ecef;
            }
            .skill-justification {
                color: #868e96;
                font-style: italic;
                font-size: 13px;
                margin-top: 8px;
                padding: 8px;
                background-color: #f8f9fa;
                border-radius: 3px;
                border-left: 3px solid #007bff;
            }
            .no-skills {
                color: #6c757d;
                font-style: italic;
                padding: 20px;
                text-align: center;
                background-color: #f8f9fa;
                border-radius: 5px;
                margin: 10px 0;
            }
            .main-header {
                text-align: center;
                color: #007bff;
                margin-bottom: 30px;
                font-size: 24px;
                font-weight: 300;
                padding-bottom: 15px;
                border-bottom: 2px solid #e9ecef;
            }
        </style>
        <div class="skill-guidelines-container">
            <h2 class="main-header">Pedoman Penilaian Skill</h2>
        """
        
        for skill_type_name, skills in skills_by_type.items():
            html_content += f"""
            <div class="skill-type-header">{skill_type_name}</div>
            """
            
            if skills:
                html_content += """
                <ul class="skill-list">
                """
                
                for skill in skills:
                    skill_name = skill.skill_id.name or 'Skill Tidak Didefinisikan'
                    skill_level = skill.skill_level_id.name or 'Level Tidak Didefinisikan'
                    justification = skill.justification or ''
                    
                    html_content += f"""
                    <li class="skill-item">
                        <div class="skill-name">{skill_name}</div>
                        <div class="skill-details">
                            <span class="skill-level">Level: {skill_level}</span>
                        </div>
                        {f'<div class="skill-justification">Justifikasi: {justification}</div>' if justification else ''}
                    </li>
                    """
                
                html_content += """
                </ul>
                """
            else:
                html_content += """
                <div class="no-skills">Tidak ada skill untuk kategori ini</div>
                """
        
        html_content += "</div>"
        return html_content
    
    def action_close(self):
        """Close the wizard"""
        return {'type': 'ir.actions.act_window_close'}
