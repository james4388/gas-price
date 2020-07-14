import React from 'react';
import PropTypes from 'prop-types';

import { Station } from './Station';

import './StationList.css';
import { Loading } from './Loading';


/**
 * Station List component
 */
function StationList({
  stations,
  isLoading
}) {
  let children = null;

  if (isLoading) {
    children = <Loading />;
  } else {
    if (stations && stations.length) {
      children = (
        <div className="result-list">
          {stations.map(station => <Station key={station.id} station={station} />)}
        </div>
      )
    } else if (stations) {
      children = <div>No stations found</div>
    }
  }

  return (
    <div className="gas-list">
      {children}   
    </div>
  )
}

StationList.propTypes = {
  stations: PropTypes.array,
  isLoading: PropTypes.bool
}

export { StationList };