import React, { useState, useEffect } from 'react';

/**
 * Hanndle application message with auto dismiss
 * @param {object} defaultMessage {message, type}
 */
export function useAppMessage(defaultMessage = null) {
  const [appMessage, setAppMessage] = useState(defaultMessage);

  useEffect(() => {
    let handle = null;

    if (appMessage && appMessage.autoDismiss) {
      handle = setTimeout(() => {
        setAppMessage(null);
      }, appMessage.autoDismiss);
    }

    return () => {
      clearTimeout(handle);
    }
  }, [appMessage]);

  return [appMessage, setAppMessage];
}