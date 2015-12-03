;(function (define) {
    'use strict';
    define(['backbone', 'js/student_profile/models/badges_model'], function(Backbone, BadgesModel) {

        var BadgesCollection = Backbone.Collection.extend({
            model : BadgesModel,
            parse: function(response) {
                console.log(response);
                return response.results;
            }
        });
        return BadgesCollection;
    });
}).call(this, define || RequireJS.define);
