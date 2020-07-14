import { useState, useEffect, useCallback } from 'react';


const defaultGeolocationOptions = {
  enableHighAccuracy: true,
  maximumAge: 0
}

export function usePosition(options=defaultGeolocationOptions) {
  const [coords, setCoords] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const onSuccess = ({ coords }) => {
    setCoords(coords);
    setError(null);
    setIsLoading(false);
  }

  const onError = (err) => {
    console.log('Error', err, new Date());
    setError(err);
    setIsLoading(false);
  }

  const requestPosition = useCallback(() => {
    console.log('Get new position from browser', new Date());
    setError(null);

    if (!navigator.geolocation) {
      setError({message: 'Geolocation is not supported'});
    } else {
      setIsLoading(true);
      navigator.geolocation.getCurrentPosition(onSuccess, onError, options);
    }
    
  }, [options])

  return [{ coords, isLoading, error }, requestPosition];
}