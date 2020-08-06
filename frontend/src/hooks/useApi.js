import { useState, useEffect } from 'react';

const { REACT_APP_API } = process.env;


/**
 * Leave returned data as is
 * @param {object} data 
 */
function identicalTransform(data) {
  return data;
}

/**
 * useFetch hook
 * TODO Support backoff???
 * @params {object} initialRequest fetch config
 */
export function useFetch(
  initialRequest = {}
) {
  const [request, setRequest] = useState(initialRequest);
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const { url, ...opts } = request;

      setError(null);
      setLoading(true);

      try {
        const result = await fetch(`${REACT_APP_API}/${url}`, opts);
        const data = await result.json();
        if (request.dataTransform) {
          setData(request.dataTransform(data));
        } else {
          setData(data);
        }

      } catch (ex) {
        setError(ex);
      }

      setLoading(false);
    };

    if (request.url) {
      fetchData();
    }
  }, [request]);

  return [{ data, error, isLoading, setData }, setRequest];
}


/**
 * Get near by gas station using current latlng
 */
export function useNearByApi() {
  const [
    { data: nearByData, isLoading: isStationLoading, error: nearByError },
    fetchNearByStation
  ] = useFetch({}, (data) => {
    return data
  });
  const [latlng, setLatLng] = useState('');
  const [fuelType, setFuelType] = useState('reg');
  const [sortBy, setSortBy] = useState('distance');
  const [distance, setDistance] = useState(5);

  useEffect(() => {
    if (latlng) {
      const url = `gasfeed/stations/near/${latlng}`;
      const params = `distance=${distance}&fuel_type=${fuelType}&sort_by=${sortBy}`;

      fetchNearByStation({
        url: `${url}?${params}`
      });
    }
  }, [latlng, distance, fuelType, sortBy, fetchNearByStation]);

  return {
    nearByData,
    nearByError,
    isStationLoading,
    setLatLng,
    fuelType,
    setFuelType,
    sortBy,
    setSortBy,
    distance,
    setDistance
  }
}

/**
 * Retrieve lat lng from address then call get nearby stations
 * @param {function} setLatLng 
 */
export function useGeocoding(setLatLng) {
  const [{ data: geocodingData, isLoading: isGeocodeLoading }, geocoding] = useFetch({});
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isGeocodeLoading) {
      setError(null);
    }
  }, [isGeocodeLoading])

  useEffect(() => {
    if (geocodingData) {
      const { results } = geocodingData;
      if (results && results.length > 0) {
        setError(null);
        const firstMatch = results[0];
        const {
          geometry: {
            location: {
              lat, lng
            }
          }
        } = firstMatch;
        setLatLng(`${lat},${lng}`);
        return;
      }
      setError('Could not find address');
    }
  }, [geocodingData, setLatLng, setError])

  return { geocoding, error };
}