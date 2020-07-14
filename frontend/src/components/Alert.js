import React from 'react';
import PropTypes from 'prop-types';

const AlertTypes = {
  PRIMARY: 'primary', 
  SECONDARY: 'secondary',
  SUCCESS: 'success', 
  DANGER: 'danger', 
  WARNING: 'warning', 
  INFO: 'info', 
  LIGHT: 'light', 
  DARK: 'dark'
};

function Alert({ clearMsg, msg }) {
  if (!msg) {
    return null;
  }
  const { message, type = AlertTypes.PRIMARY } = msg;

  return <div className={`alert alert-${type}`} role="alert">
    {message}
    <button type="button" className="close" aria-label="Close" onClick={clearMsg}>
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
}

Alert.propTypes = {
  msg: PropTypes.shape({
    message: PropTypes.string,
    type: PropTypes.oneOf(Object.values(AlertTypes))
  }),
  clearMsg: PropTypes.func
}

export { Alert, AlertTypes };