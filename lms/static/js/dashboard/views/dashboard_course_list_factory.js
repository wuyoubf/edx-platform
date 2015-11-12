;(function (define) {
    'use strict';

    define(['js/dashboard/views/course_list_tabbed_view'],
        function (CourseListTabbedView) {
            return function (currentCourses, archivedCourses, courseSettings) {
                new CourseListTabbedView(currentCourses, archivedCourses, courseSettings).render();
            };
        });
}).call(this, define || RequireJS.define);
