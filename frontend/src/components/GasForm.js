import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

import { AlertTypes, Alert } from './Alert';
import { FUELTYPES, DISTANCES } from '../mock/options';
import { usePosition } from '../hooks/usePosition';

import './GasForm.css';

const CURRENT_LOCATION = 'current location';

/**
 * GasForm component
 */
function GasForm({
  onLatLngChange,
  onQueryChange,
  fuelType,
  onFuelTypeChange,
  setAppMessage
}) {
  const [
    { coords, isLoading: isPositionLoading, error: locationError },
    getPosition
  ] = usePosition();
  const [query, setQuery] = useState('');

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  }

  useEffect(() => {
    if (locationError) {
      setAppMessage({message: locationError.message, type: AlertTypes.DANGER});
    }
  }, [locationError, setAppMessage]);

  const handleGetPosition = () => {
    setAppMessage({
      message: 'Pinpoint your location, please allow Geolocation permission', 
      type: AlertTypes.INFO,
      autoDismiss: 5000
    });
    setQuery(CURRENT_LOCATION);
    getPosition();
  }

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (query && query !== CURRENT_LOCATION) {
      onQueryChange(query);
    }
    return false;
  }

  const handleFuelTypeChange = (e) => {
    onFuelTypeChange(e.target.value);
  }

  useEffect(() => {
    if (coords && coords.latitude && coords.longitude) {
      onLatLngChange(`${coords.latitude},${coords.longitude}`);
    }
  }, [coords, onLatLngChange])

  return (
    <div className="gas-form">
      <form onSubmit={handleFormSubmit}>

        <div className="form-group">
          <label htmlFor="query">Search gas price</label>
          <div className="input-group mb-3">
            <input
              value={query}
              onChange={handleQueryChange}
              type="text"
              className="form-control form-control-lg"
              id="query"
              aria-describedby="queryHelp" />
            <div className="input-group-append">
              <button
                onClick={handleGetPosition}
                disabled={isPositionLoading}
                className="btn btn-success"
                type="button"
                title="Current location"
              >
                {isPositionLoading ?
                  <span className="loading"><i className="fas fa-spinner"></i></span>
                  :
                  <i className="fas fa-crosshairs"></i>
                }
              </button>
            </div>
          </div>
          <small id="queryHelp" className="form-text text-muted">
            Search gas price by city or zipcode
          </small>
        </div>

        <div className="row">
          <div className="form-group col">
            <label htmlFor="inputFuelType">Fuel Type</label>
            <select
              id="inputFuelType"
              className="form-control"
              value={fuelType}
              onChange={handleFuelTypeChange}
            >
              {
                FUELTYPES.map(
                  ([value, label]) =>
                    <option key={value} value={value}>{label}</option>
                )
              }
            </select>
          </div>

          <div className="col">
            <label htmlFor="inputDistance">Distance</label>
            <select
              disabled={true}
              title="Not yet implemented"
              id="inputDistance"
              className="form-control"
            >
              {
                DISTANCES.map(
                  ([value, label]) =>
                    <option key={value} value={value}>{label}</option>
                )
              }
            </select>
          </div>
          <div className="col">
            <label htmlFor="inputSortBy">Sort by</label>
            <select
              disabled={true}
              title="Not yet implemented"
              id="inputSortBy"
              className="form-control"
            >
              <option value="price">Price</option>
              <option value="distance">Distance</option>
            </select>
          </div>
        </div>

        <input
          type="submit"
          disabled={!query}
          className="btn btn-primary btn-lg btn-block" value="Find Gas" />
      </form>
    </div>
  )
}


GasForm.propTypes = {
  onLatLngChange: PropTypes.func,
  onQueryChange: PropTypes.func,
  fuelType: PropTypes.string,
  onFuelTypeChange: PropTypes.func,
  setAppMessage: PropTypes.func
};

export { GasForm };