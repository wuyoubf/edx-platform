define([
        'backbone',
        'jquery',
        'js/financial-assistance/views/financial_assistance_form_view'
    ], function (Backbone, $, FinancialAssistanceFormView) {
        
        'use strict';
        
        describe('Financial Assistance View', function () {
            var view = null,
                context = {
                    fields: [{
                        defaultValue: '',
                        form: 'financial-assistance',
                        instructions: 'select a course',
                        label: 'Course',
                        name: 'course',
                        options: [
                            {'name': 'Verified with Audit', 'value': 'course-v1:HCFA+VA101+2015'},
                            {'name': 'Something Else', 'value': 'course-v1:SomethingX+SE101+215'},
                            {'name': 'Test Course', 'value': 'course-v1:TestX+T101+2015'}
                        ],
                        placeholder: '',
                        required: true,
                        requiredStr: '',
                        type: 'select'
                    }],
                    user_details: {
                        country: 'UK',
                        email: 'xsy@edx.org',
                        name: 'xsy',
                        username: 'xsy4ever'
                    },
                    header_text: ['Line one.', 'Line two.'],
                    student_faq_url: '/faqs',
                    dashboard_url: '/dashboard',
                    platform_name: 'edx',
                    submit_url: '/api/financial/v1/assistance'
                };

            beforeEach(function() {
                setFixtures('<div class="financial-assistance-wrapper"></div>');
                view = new FinancialAssistanceFormView({
                    el: '.financial-assistance-wrapper',
                    context: context
                });
            });

            afterEach(function() {
                view.undelegateEvents();
                view.remove();
            });

            it('should exist', function() {
                expect(view).toBeDefined();
            });

            xit('should load the form based on passed in context', function() {

            });

            xit('should not submit the form if the front end validation fails', function() {

            });

            xit('should submit the form data and additional data if validation passes', function() {

            });

            xit('should submit the form and show a success message if content is valid and API returns success', function() {

            });

            xit('should submit the form and show an error message if content is valid and API returns error', function() {

            });

            xit('should allow form resubmission after a front end validation failure', function() {

            });

            xit('should allow form resubmission after an API error is returned', function() {

            });
        });
    }
);
