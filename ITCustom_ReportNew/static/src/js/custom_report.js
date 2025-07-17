/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const { Component } = owl;

class CustomReportFormController extends Component {
    setup() {
        this.actionService = useService("action");
    }

    async onPrintReport() {
        const record = this.props.record;
        const result = await this.env.services.rpc({
            model: 'custom.report',
            method: 'print_report',
            args: [record.resId],
        });
        this.actionService.doAction(result);
    }
}

CustomReportFormController.template = "ITCustom_ReportNew.CustomReportForm";
registry.category("form").add("custom_report_form", CustomReportFormController);
