import React from 'react';
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import { Loading } from './Loading';

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

it('render loading icon', async () => {
  await act(async () => {
    render(<Loading />, container);
  });
  expect(container.innerHTML).toContain('fas fa-spinner');
})
