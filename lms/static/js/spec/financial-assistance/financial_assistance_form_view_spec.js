define([
        'backbone',
        'jquery',
        'js/financial-assistance/views/financial_assistance_form_view'
    ], function (Backbone, $, FinancialAssistanceFormView) {
        
        'use strict';
        
        describe('Financial Assistance View', function () {
            var view = null,
                context = {
                    fields: [
                        {
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
                        }, {
                            defaultValue: '',
                            instructions: 'Specify your annual income in USD.',
                            label: 'Annual Income',
                            name: 'income',
                            placeholder: 'income in USD ($)',
                            required: true,
                            restrictions: {},
                            type: 'text'
                        }, {
                            defaultValue: '',
                            instructions: 'Use between 250 and 500 words or so in your response.',
                            label: 'Tell us about your current financial situation, including any unusual circumstances.',
                            name: 'reason_for_applying',
                            placeholder: '',
                            required: true,
                            restrictions: {
                                max_length: 2500,
                                min_length: 800
                            },
                            type: 'textarea'
                        }, {
                            defaultValue: '',
                            instructions: "Use between 250 and 500 words or so in your response."
                            label: "Tell us about your learning or professional goals. How will a Verified Certificate in this course help you achieve these goals?"
                            name: "goals"
                            placeholder: '',
                            required: true
                            restrictions: Object
                            max_length: 2500
                            min_length: 800,
                            type: 'textarea'
                        }, {
                            defaultValue: '',
                            instructions: "Use between 250 and 500 words or so in your response."
                            label: "Tell us about your plans for this course. What steps will you take to help you complete the course work a receive a certificate?"
                            name: "effort"
                            placeholder: '',
                            required: true
                            restrictions: Object
                            max_length: 2500
                            min_length: 800,
                            type: 'textarea'
                        }, {
                            defaultValue: '',
                            instructions: 'Annual income and personal information such as email address will not be shared.',
                            label: 'I allow edX to use the information provided in this application for edX marketing purposes.',
                            name: 'mktg-permission',
                            placeholder: '',
                            required: false,
                            restrictions: {},
                            type: 'checkbox'
                        }
                    ],
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
