import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import React from 'react';

const Button = ({ text, icon, isActive, onClick, className, disabled = false, ...props }) => {
    return (
        <button
            {...props}
            disabled={disabled}
            onClick={onClick}
            className={className + `${disabled ? ' opacity-50' : ' opacity-100'}` + ` inline-flex items-center justify-center py-1 px-3 rounded-lg transition duration-300 ${isActive ? 'bg-primary text-white' : 'bg-gray-200 text-primary hover:bg-gray-300'
                }`}
        >
            {icon != null &&
                <FontAwesomeIcon icon={icon} className={`${text != null ? 'mr-2' : ''}`} />
            }
            {text != null &&
                <p className='block'>
                    {text}
                </p>
            }
        </button>
    );
};

export default Button;
