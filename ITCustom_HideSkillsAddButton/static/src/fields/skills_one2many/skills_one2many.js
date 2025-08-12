/** @odoo-module **/

import { SkillsListRenderer } from '@hr_skills/fields/skills_one2many/skills_one2many';

export class SkillsListRendererPatched extends SkillsListRenderer {
    /**
     * Override to hide ADD buttons
     */
    setup() {
        super.setup();
    }

    /**
     * Hide ADD buttons by overriding the template
     */
    get recordRowTemplate() {
        return 'web.ListRenderer.Rows';
    }

    /**
     * Override to hide ADD buttons in skill groups
     */
    get groupedList() {
        const result = super.groupedList;
        // Hide ADD buttons by removing the button elements
        Object.keys(result).forEach(key => {
            if (result[key] && result[key].list) {
                // Remove ADD button functionality
                result[key].showAddButton = false;
            }
        });
        return result;
    }
}

SkillsListRenderer.template = 'ITCustom_HideSkillsAddButton.SkillsListRenderer';
SkillsListRenderer.components = {
    ...SkillsListRenderer.components,
    SkillsListRenderer: SkillsListRendererPatched,
};
