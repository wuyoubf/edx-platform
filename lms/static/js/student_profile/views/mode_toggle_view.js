;(function (define, undefined) {
    'use strict';
    define([
            'gettext', 'jquery', 'underscore', 'backbone'],
        function (gettext, $, _, Backbone) {

            var ModeToggleView = Backbone.View.extend({
                tagName: 'ul',
                initialize: function(options) {
                    var self = this;
                    this.profile = options['profile'];  // JQuery Selector
                    this.badges = options['badges'];  // Backbone View
                    this.sections = $([this.profile[0], this.badges.el]);
                    this.profile_toggle = $('.profile-toggle');
                    this.accomplishments_toggle = $('.accomplishments-toggle');
                    function setToggle(event) {
                        var target = $(event.target);
                        self.$el.find('*').removeClass('is-active');
                        target.addClass('is-active');
                        self.sections.hide();
                        event.data['section'].show();
                    }
                    this.profile_toggle.click({'section': this.profile}, setToggle);
                    this.accomplishments_toggle.click({'section': this.badges.$el}, setToggle);
                },
                render: function () {
                    if (this.badges.collection.size() == 0) {
                        // No badges, therefore nothing to show.
                        return this
                    }
                    this.badges.$el.hide();
                    this.badges.render();
                    this.$el.show();
                    return this;
                }
            });

            return ModeToggleView;
        });
}).call(this, define || RequireJS.define);
