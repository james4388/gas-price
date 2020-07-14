import React from 'react';
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import { CompanyLogo } from './CompanyLogo';

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

it('hide img if not found', async () => {
  await act(async () => {
    render(<CompanyLogo companyName="{---we-r-ew-}" />, container);
  });
  expect(container.getElementsByTagName('img').length).toBe(0);
})
