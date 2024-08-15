import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';

const Loader = () => {
    return (
        <div className='h-full flex justify-center items-center' >
            <FontAwesomeIcon icon={faSpinner} spin size='3x' />
        </div>
    );
};

export default Loader;