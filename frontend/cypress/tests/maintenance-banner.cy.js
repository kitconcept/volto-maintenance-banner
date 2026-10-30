import { ploneAuth } from '@plone/volto/cypress/support/constants';

const API_URL =
  Cypress.env('API_PATH') ||
  `http://${Cypress.env('BACKEND_HOST') || '127.0.0.1'}:55001/${
    Cypress.env('SITE_ID') || 'plone'
  }`;

const setBanner = (values) =>
  cy.request({
    method: 'PATCH',
    url: `${API_URL}/@controlpanels/maintenance-banner`,
    headers: { Accept: 'application/json' },
    auth: { user: ploneAuth[0], pass: ploneAuth[1] },
    body: values,
  });

context('Maintenance Banner Acceptance Tests', () => {
  beforeEach(() => {
    cy.viewport('macbook-16');
    cy.intercept('GET', '/**/@maintenance-banner').as('banner');
  });

  describe('Banner disabled', () => {
    it('As anonymous I do not see the banner', function () {
      cy.visit('/');
      cy.wait('@banner');
      cy.get('.maintenance-banner').should('not.exist');
    });
  });

  describe('Banner enabled', () => {
    beforeEach(() => {
      setBanner({
        show_banner: true,
        banner_title: 'Scheduled maintenance',
        banner_text: 'The site will be down for maintenance.',
        date: '2026-10-31',
      });
    });

    it('As anonymous I see the banner with title, date and text', function () {
      cy.visit('/');
      cy.wait('@banner');
      cy.get('.maintenance-banner')
        .should('be.visible')
        .and('have.attr', 'role', 'alert');
      cy.get('.maintenance-banner-title').should(
        'have.text',
        'Scheduled maintenance',
      );
      cy.get('.maintenance-banner-date').should('contain', 'October 31, 2026');
      cy.get('.maintenance-banner section').should(
        'contain',
        'The site will be down for maintenance.',
      );
    });

    it('As editor I see the banner above the header', function () {
      cy.autologin();
      cy.visit('/');
      cy.wait('@banner');
      cy.get('.maintenance-banner').should('be.visible');
      cy.get('.maintenance-banner')
        .nextAll('.header-wrapper')
        .should('have.length', 1);
    });
  });

  describe('Control panel', () => {
    it('As admin I can find the maintenance banner control panel', function () {
      cy.autologin();
      cy.visit('/controlpanel');
      cy.get('a[href="/controlpanel/maintenance-banner"]').should('exist');
    });

    it('As admin I can enable the banner in the control panel and see it', function () {
      cy.intercept('PATCH', '/**/@controlpanels/maintenance-banner').as('save');
      cy.autologin();
      cy.visit('/controlpanel/maintenance-banner');

      cy.get('label[for="field-show_banner"]').click();
      cy.get('#field-banner_title').clear().type('Edited in control panel');
      cy.get('.field-wrapper-banner_text [contenteditable="true"]')
        .click()
        .type('Banner text from the control panel');
      cy.get('#toolbar-save').click();
      cy.wait('@save').its('response.statusCode').should('eq', 204);

      cy.navigate('/');
      cy.wait('@banner');
      cy.get('.maintenance-banner').should('be.visible');
      cy.get('.maintenance-banner-title').should(
        'have.text',
        'Edited in control panel',
      );
      cy.get('.maintenance-banner section').should(
        'contain',
        'Banner text from the control panel',
      );
    });
  });
});
