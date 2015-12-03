;(function (define, undefined) {
    'use strict';
    define([
            'gettext', 'jquery', 'underscore', 'backbone', 'js/student_profile/views/badge_view',
            'text!templates/student_profile/badge_placeholder.underscore'],
        function (gettext, $, _, Backbone, BadgeView, badgePlaceholder) {

            var BadgeListingView = Backbone.View.extend({
                initialize: function (options) {
                    this.find_courses_url = options.find_courses_url;
                },
                render: function () {
                    var grid = $('<div class="badge-set-display">');
                    var row;
                    this.collection.each(function (badge, index, collection) {
                        if (! (index % 2) ) {
                            row = $("<div class='badge-row'>");
                            grid.append(row)
                        }
                        row.append(new BadgeView({model: badge}).render().el);
                        if ((index + 1) == collection.length) {
                            if (index % 2) {
                                row = $("<div class='badge-row'>");
                                grid.append(row)
                            }
                            row.append(_.template(badgePlaceholder,  {'find_courses_url': this.find_courses_url}))
                        }
                    }, this);
                    this.$el.html(grid);
                    return this;
                }
            });

            return BadgeListingView;
        });
}).call(this, define || RequireJS.define);
