import React from 'react';
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import { Station } from './Station';

let container = null;
beforeEach(() => {
  container = document.createElement("div");
  document.body.appendChild(container);
});

afterEach(() => {
  unmountComponentAtNode(container);
  container.remove();
  container = null;
});

it('render station with info', async () => {
  const station = {
    "address": "7360 La Tijera Blvd", 
    "city": "Los Angeles", 
    "country": "United States", 
    "diesel": "1", 
    "diesel_date": "5 years ago", 
    "diesel_price": "N/A", 
    "distance": "0.4 miles", 
    "id": "95612", 
    "lat": "33.971275", 
    "lng": "-118.378593", 
    "mid_date": "5 years ago", 
    "mid_price": "4.03", 
    "pre_date": "5 years ago", 
    "pre_price": "4.13", 
    "reg_date": "5 years ago", 
    "reg_price": "3.89", 
    "region": "California", 
    "station": "Chevron", 
    "zip": "90045"
  }

  await act(async () => {
    render(<Station station={station} />, container);
  });
  expect(container.innerHTML).toContain('7360 La Tijera Blvd');
  expect(container.innerHTML).toContain('0.4 miles');
})
