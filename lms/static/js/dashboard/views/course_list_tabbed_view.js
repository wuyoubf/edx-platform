;(function (define) {
    'use strict';

    define(['backbone', 'underscore', 'gettext',
        'js/dashboard/routers/dashboard_router',
        'js/dashboard/models/settings',
        'js/dashboard/collection/courses',
        'js/dashboard/views/course_list_view',
        'js/dashboard/views/course_view',
        'js/components/tabbed/views/tabbed_view'
    ], function (Backbone, _, gettext, DashboardRouter, Settings, CourseCollection,
                 CourseListView, CourseView, TabbedView) {

        var CourseListTabbedView = Backbone.View.extend({

            el: '.wrapper-header-courses',

            courses: {
                current: {
                    title: gettext('Current'),
                    url: '/courses/current',
                    index: 0
                },
                archived: {
                    title: gettext('Archived'),
                    url: '/courses/archived',
                    index: 1
                }
            },

            initialize: function (currentCourses, archivedCourses, courseSettings) {

                var router = new DashboardRouter(),
                    dispatcher = _.clone(Backbone.Events),
                    settingsModel = new Settings(courseSettings);

                dispatcher.listenTo(router, 'goToTab', _.bind(function (tab) {
                    this.goToTab(tab);
                }, this));

                this.setElement(this.el);

                this.currentCourseListView = new CourseListView({
                    template: this.courses.current.template,
                    itemViewClass: CourseView,
                    parent: this,
                    collection: new CourseCollection(currentCourses),
                    settingsModel: settingsModel
                });
                this.archivedCourseListView = new CourseListView({
                    template: this.courses.archived.template,
                    itemViewClass: CourseView,
                    parent: this,
                    collection: new CourseCollection(archivedCourses),
                    settingsModel: settingsModel
                });

                this.mainView = new TabbedView({
                    tabs: [{
                        title: this.courses.current.title,
                        url: this.courses.current.url,
                        view: this.currentCourseListView
                    }, {
                        title: this.courses.archived.title,
                        url: this.courses.archived.url,
                        view: this.archivedCourseListView
                    }],
                    router: router
                });

                Backbone.history.start();
            },

            render: function () {
                this.mainView.setElement(this.el).render();

                this.trigger('rendered');
                return this;
            },

            /**
             * Set up the tabbed view and switch tabs.
             */
            goToTab: function (tab) {

                // Note that `render` should be called first so
                // that the tabbed view's element is set
                // correctly.
                var tabId = tab.split('-')[0];
                this.render();
                this.mainView.setActiveTab(this.courses[tabId].index);
            }

        });

        return CourseListTabbedView;
    });

}).call(this, define || RequireJS.define);
