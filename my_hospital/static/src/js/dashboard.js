odoo.define('dashboard.Dashboard', function (require) {
'use strict';

var AbstractAction = require('web.AbstractAction');
var core=require('web.core');

var myDashboard=AbstractAction.extend({
template:'Dashboard',
core.action_registry.add('custom_dashboard_tag',myDashboard)
})
core.action_registry.add('custom_dashboard_tag', myDashboard);
return myDashboard;

});