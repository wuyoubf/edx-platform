;(function (define) {
    'use strict';

    define(['backbone', 'js/dashboard/models/course'], function (Backbone, Course) {
        return Backbone.Collection.extend({
            model: Course
        });
    });

}).call(this, define || RequireJS.define);
