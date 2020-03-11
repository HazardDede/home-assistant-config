import {
    LitElement, html
  } from 'https://unpkg.com/@polymer/lit-element@^0.5.2/lit-element.js?module';
  
  class PlantSensorCard extends LitElement {
    static get properties() {
      return {
        hass: Object,
        config: Object,
        state: Object,
        dashArray: String,
        outsideLimits: Number
      }
    }
  
    _render({ state, dashArray, outsideLimits, config }) {
      return html`
      <style>
          :host {
            cursor: pointer;
          }

          .container {
            position: relative;
            height: 100%;
            display: flex;
            flex-direction: column;
          }

          .labelContainer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
          }

          .text {
            font-size: 100%;
            margin-top: 0px;
            margin-bottom: 0px;
          }
          
          .unit {
            margin-top: 5%;
            margin-bottom: 0px;
            font-size: 75%;
            padding: 0.05em 0.6em 0.05em 0.6em;
            border-radius: 100px;
          }

      </style>
      <div class="container" id="container" on-click="${() => this._click()}">
        <svg viewbox="0 0 200 200" id="svg">
          <circle id="circle" cx="50%" cy="50%" r="45%"
            fill$="${config.fill || 'rgba(255, 255, 255, .75)'}"
            stroke$="${outsideLimits ? config.warn_color || '#f20707' : config.ok_color || '#0c870c'}"
            stroke-dasharray$="${dashArray}"
            stroke-width$="${config.stroke_width || 6}" 
            transform="rotate(-90 100 100)"/>
        </svg>
        <span class="labelContainer">
          <p class="text">
            ${config.attribute ? state.attributes[config.attribute] : state.state}
          </p>
          <p class="unit" style="background-color: ${outsideLimits ? config.warn_color || '#f20707' : config.ok_color || '#0c870c'}">
            ${config.units ? config.units : state.attributes.unit_of_measurement}
          </p>
        </span>
      </div>
      `;
    }
  
    _createRoot() {
      const shadow = this.attachShadow({ mode: 'open' })
      if (!this.config.show_card) {
        return shadow;
      }
      const card = document.createElement('ha-card');
      shadow.appendChild(card);
      return card;
    }
  
    _didRender() {
      this.circle = this._root.querySelector('#circle');
      if (this.config) {
        this._updateConfig();
      }
    }
  
    setConfig(config) {
      if (!config.entity) {
        throw Error('No entity defined')
      }
      this.config = config;
      if (this.circle) {
        this._updateConfig();
      }
    }
  
    getCardSize() {
      return 3;
    }
  
    _updateConfig() {
      const container = this._root.querySelector('.labelContainer');
      container.style.color = 'var(--primary-text-color)';
  
      if (this.config.font_style) {
        Object.keys(this.config.font_style).forEach((prop) => {
          container.style.setProperty(prop, this.config.font_style[prop]);
        });
      }
    }
  
    set hass(hass) {
      this.state = hass.states[this.config.entity];
  
      if (this.config.attribute) {
        if (!this.state.attributes[this.config.attribute] ||
            isNaN(this.state.attributes[this.config.attribute])) {
          console.error(`Attribute [${this.config.attribute}] is not a number`);
          return;
        }
      } else {
        if (!this.state || isNaN(this.state.state)) {
          console.error(`State is not a number`);
          return;
        }
      }
  
      const state = this.config.attribute
        ? this.state.attributes[this.config.attribute]
        : this.state.state;
      const r = 200 * .45;
      const min = this.config.min || 0;
      const max = this.config.attribute_max
        ? this.state.attributes[this.config.attribute_max]
        : (this.config.max || 100);
      const val = this._calculateValueBetween(min, max, state);
      const score = val * 2 * Math.PI * r;
      const total = 10 * r;
      this.dashArray = `${score} ${total}`;
      
      this.outsideLimits = !(state >= min && state <= max)
    }
  
    _click() {
      this._fire('hass-more-info', { entityId: this.config.entity });
    }
  
    _calculateValueBetween(start, end, val) {
      const res = (val - start) / (end - start);
      return res < 0 ? 0 : res
    }
  
    _fire(type, detail) {
      const event = new Event(type, {
        bubbles: true,
        cancelable: false,
        composed: true
      });
      event.detail = detail || {};
      this.shadowRoot.dispatchEvent(event);
      return event;
    }
  }
  customElements.define('plant-sensor-card', PlantSensorCard);