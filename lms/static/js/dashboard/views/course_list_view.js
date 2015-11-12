;(function (define) {
    'use strict';

    define(['jquery', 'underscore', 'common/js/components/views/list', 'text!templates/dashboard/courses.underscore'],
        function ($, _, ListView, coursesTemplate) {

            var CourseListView = ListView.extend({

                initialize: function (options) {
                    this.itemViewClass = options.itemViewClass || this.itemViewClass;
                    this.template = _.template(coursesTemplate);
                    this.parent = options.parent;
                    this.settingsModel = options.settingsModel;
                    this.itemViews = [];
                },

                render: function () {
                    this.$el.html(this.template({courses: this.collection, settings: this.settingsModel}));
                    this.collection.each(this.createItemView, this);

                    return this;
                },

                createItemView: function (course) {
                    var itemView = new this.itemViewClass({
                        model: course,
                        settingsModel: this.settingsModel,
                        tabbedView: this.parent
                    });

                    this.$('.listing-courses').append(itemView.render().el);
                    this.itemViews.push(itemView);
                }
            });

            return CourseListView;
        });

}).call(this, define || RequireJS.define);
