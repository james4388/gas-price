import React, { useState, useEffect } from 'react';
import './App.css';

import { GasForm } from './components/GasForm';
import { StationList } from './components/StationList';
import { AlertTypes, Alert } from './components/Alert';

import { useNearByApi, useGeocoding } from './hooks/useApi';
import { useAppMessage } from './hooks/useAppMessage';
import { isLatLngPair } from './utils/stringUtil';


function App() {
  const [appMessage, setAppMessage] = useAppMessage(null);
  const {
    nearByData,
    nearByError,
    isStationLoading,
    setLatLng,
    fuelType,
    setFuelType,
  } = useNearByApi();
  const { geocoding, error: geoCodingError } = useGeocoding(setLatLng);
  const [query, setQuery] = useState('');
  const [stations, setStations] = useState(null);

  // Watch changes from query or geocoding
  useEffect(() => {
    if (query) {
      if (isLatLngPair(query)) {
        setLatLng(query);
      } else {
        geocoding({
          url: `/geocoding/address/${query}`
        });
      }
    }
  }, [query, geocoding, setLatLng]);

  // Handle geocoding error
  useEffect(() => {
    if (geoCodingError) {
      setAppMessage({
        message: geoCodingError, 
        type: AlertTypes.WARNING,
        autoDismiss: 5000
      });
    }
  }, [geoCodingError]);

  const clearAppMessage = () => {
    setAppMessage(null);
  }

  return (
    <div className="container-fluid App">
      <div className="header">
        <h3><i className="fas fa-gas-pump"></i> Gas Price</h3>
      </div>

      <div className="row">

        <div className="left-col col-md-8">
          <Alert msg={appMessage} clearMsg={clearAppMessage} />

          <GasForm
            onLatLngChange={setLatLng}
            onQueryChange={setQuery}
            fuelType={fuelType}
            onFuelTypeChange={setFuelType}
            setAppMessage={setAppMessage}
          />

          <StationList 
            stations={nearByData && nearByData.stations} 
            isLoading={isStationLoading}  
          />

        </div>

        <div className="right-col col-md-4 d-none d-md-block d-lg-block">
          Advertisement goes here :)
          <img
            className="img-fluid"
            src="https://via.placeholder.com/400.png?text=Adverstise" 
            alt="Ads"
          />
        </div>

      </div>

      <div className="footer">
        &copy; 2020 <a href="https://nhutrinh.com">Nhu Trinh</a>.
        Gas api from <a href="http://www.mygasfeed.com/">mygasfeed.com</a>
      </div>
    </div>
  );
}

export default App;
