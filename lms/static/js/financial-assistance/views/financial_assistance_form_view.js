;(function (define) {
    'use strict';

    define(['backbone',
            'jquery',
            'underscore',
            'gettext',
            'js/financial-assistance/models/financial_assistance_model',
            'text!js/financial-assistance/templates/financial_assessment_form.underscore',
            'text!js/financial-assistance/templates/financial_assessment_submitted.underscore',
            'js/student_account/views/FormView',
            'text!templates/student_account/form_field.underscore'
         ],
         function(Backbone, $, _, gettext, FinancialAssistanceModel, formViewTpl, successTpl, FormView, formFieldTpl ) {
         	return FormView.extend({
         		el: '.financial-assistance-wrapper',
         		events: {
	                'click .js-submit-form': 'submitForm'
	            },
         		tpl: formViewTpl,
         		fieldTpl: formFieldTpl,
         		formType: 'financial-assistance',
         		requiredStr: '',
         		submitButton: '.js-submit-form',

         		initialize: function(data) {
					var context = data.context,
						fields = context.fields;

					// Add default option to array
					if ( fields[0].options.length > 1 ) {
						fields[0].options.unshift({
							name: '- ' + gettext('Choose one') + ' -',
							value: '',
							default: true
						});
					}

					// Set non-form data needed to render the View
					this.context = {
						dashboard_url: context.dashboard_url,
						header_text: context.header_text,
						platform_name: context.platform_name,
						student_faq_url: context.student_faq_url
					};

					// Make the value accessible to this View
					this.user_details = context.user_details;

	                // Initialize the model and set user details
	                this.model = new FinancialAssistanceModel({
	                	url: context.submit_url
	                });
	                this.model.set( context.user_details );
	                this.listenTo( this.model, 'error', this.saveError );
	                this.model.on('sync', this.renderSuccess, this);
	                
	                // Build the form
	                this.buildForm( fields );
	            },

	            render: function(html) {
	                var fields = html || '',
	                	data = _.extend( this.model.toJSON(), this.context, {
	                    	fields: html || '',
	                	});

	                this.$el.html(_.template(this.tpl, data));

	                this.postRender();

	                return this;
	            },

	            failedSubmission: function() {
	            },

	            renderSuccess: function() {
	            	this.$el.html(_.template(successTpl, {
	            		course: this.model.get('course'),
	            		dashboard_url: this.context.dashboard_url
	            	}));
	            },

	            saveError: function(error) {
	            	var msg = gettext('An error has occurred. Wait a few minutes and then try to submit the application again. If you continue to have issues please contact support.');
	                if (error.status === 0) {
	                    msg = gettext('An error has occurred. Check your Internet connection and try again.');
	                }
	                this.errors = ['<li>' + msg + '</li>'];
	                this.setErrors();
	                this.element.hide( this.$resetSuccess );
	            },

	            setExtraData: function(data) {
	            	return _.extend(data, this.user_details);
	            }
         	});
        }
    );
}).call(this, define || RequireJS.define);
