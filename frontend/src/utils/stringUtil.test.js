import { getInitial, isLatLngPair } from './stringUtil';

it('Make initial from name', () => {
  expect(getInitial('Hello world')).toEqual('HW');
  expect(getInitial('ab')).toEqual('AB');
  expect(getInitial('   space   another   ')).toEqual('SA');
  expect(getInitial('First mid mid mid mid Last')).toEqual('FL');
  expect(getInitial('a')).toEqual('A');
});

it('Test is latitude, longitude string', () => {
  expect(isLatLngPair('12.3456, 45.678')).toBe(true);
  expect(isLatLngPair('12.3456 45.678')).toBe(false);
  expect(isLatLngPair('asd asds 8')).toBe(false);
  expect(isLatLngPair('-90.512, 35.22')).toBe(false);
  expect(isLatLngPair('-90.000, -180.000')).toBe(true);
  expect(isLatLngPair('-90.000, -181.000')).toBe(false);
})