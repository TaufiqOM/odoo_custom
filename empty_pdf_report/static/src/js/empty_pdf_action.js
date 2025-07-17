/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class EmptyPDFAction extends Component {
    setup() {
        // Open the PDF report in a new tab
        const url = '/empty_pdf_report/generate';
        window.open(url, '_blank');
        
        // Close the current window/tab
        setTimeout(() => {
            window.close();
        }, 100);
    }
}

registry.category("actions").add("empty_pdf_report.action", EmptyPDFAction);
