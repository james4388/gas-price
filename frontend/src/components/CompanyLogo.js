import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { getInitial } from '../utils/stringUtil';

import './CompanyLogo.css';

const { REACT_APP_API } = process.env;


function CompanyLogo({
  companyName
}) {
  const [hideLogo, setHideLogo] = useState(false);

  useEffect(() => {
    setHideLogo(false);
  }, [companyName]);

  return (
    <div className="logo">
      <div className="logo-img">

        {!hideLogo ?
          <img
            onError={() => setHideLogo(true)}
            className="logo-img"
            src={`${REACT_APP_API}/clearbit/logo/${companyName}`}
            alt="avatar" />
          :
          getInitial(companyName)
        }

      </div>
    </div>
  )
}

CompanyLogo.propTypes = {
  companyName: PropTypes.string.isRequired
}

export { CompanyLogo };