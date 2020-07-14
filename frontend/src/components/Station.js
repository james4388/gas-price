import React, { useState, useEffect } from 'react';
import { CompanyLogo } from './CompanyLogo';

import './Station.css';

/**
 * Station component
 */
export function Station({station={}, fuelType = 'reg'}) {
  const fullAddress = `${station.address}, ${station.city}, ${station.region}, ${station.zip}`;

  return (
    <a href={`https://www.google.com/maps/dir//${fullAddress}`} target="_blank">
      <div className="list-item">
        <CompanyLogo companyName={station.station} />

        <div className="price">
          <h3>${station[`${fuelType}_price`]}</h3>
          <div className="other-price">
            {station[`${fuelType}_date`]}
          </div>
        </div>
        <div className="info">
          <h5>{station.station}</h5>
          <p className="distance">{station.distance}</p>
          <p className="address">
            <i className="fas fa-map-marker-alt"></i>&nbsp;
            <span>{station.address}</span><br />
            <span>{station.city}, {station.region}, {station.zip}</span>
          </p>
        </div>
      </div>
    </a>
  )
}