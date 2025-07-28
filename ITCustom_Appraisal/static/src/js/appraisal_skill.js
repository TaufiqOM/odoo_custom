odoo.define('appraisal_skill_custom.GroupSkill', function (require) {
    "use strict";
    
    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var viewRegistry = require('web.view_registry');
    
    var AppraisalSkillFormController = FormController.extend({
        _onButtonClicked: function (ev) {
            if (ev.data.attrs.special === 'save_custom_group') {
                this._saveCustomGroup();
            } else {
                this._super.apply(this, arguments);
            }
        },
        
        _saveCustomGroup: function () {
            var self = this;
            var record = this.model.get(this.handle);
            var groupName = record.data.custom_group;
            
            if (!groupName) {
                this.do_warn("Warning", "Please enter a group name");
                return;
            }
            
            this._rpc({
                model: 'appraisal.skill.group',
                method: 'create',
                args: [{'name': groupName}],
            }).then(function (groupId) {
                self._rpc({
                    model: 'hr.appraisal.skill',
                    method: 'write',
                    args: [[record.res_id], {'group_id': groupId, 'custom_group': False}],
                }).then(function () {
                    self.reload();
                });
            });
        }
    });
    
    var AppraisalSkillFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: AppraisalSkillFormController,
        }),
    });
    
    viewRegistry.add('appraisal_skill_form', AppraisalSkillFormView);
});