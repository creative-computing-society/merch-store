import React, { useState, useContext } from 'react';
import { faX, faBars } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import ccs_bulb from '../assets/CCS_Bulb.png';
import AuthContext from '../helpers/AuthContext';
import { Link } from 'react-router-dom';
import Button from './Button';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
    const navigate = useNavigate();

    const [isDropdownVisible, setIsDropdownVisible] = useState(false);
    const [isHelpModalVisible, setIsHelpModalVisible] = useState(false);
    const authCtx = useContext(AuthContext);

    const toggleDropdown = () => {
        setIsDropdownVisible(!isDropdownVisible);
    };

    const handleLogout = () => {
        setIsDropdownVisible(false);
        authCtx.logout();
    };

    const handleHelp = () => {
        // Add help functionality here
        setIsDropdownVisible(false);
        setIsHelpModalVisible(!isHelpModalVisible);
    };

    const handlePolicies = () => {
        navigate('/policies');
        setIsDropdownVisible(!isDropdownVisible);
    };

    return (<>
        <div className={`${isHelpModalVisible ? "flex" : "hidden"} fixed z-50 inset-0 bg-black bg-opacity-50 items-center justify-center`}>
            <div className="bg-white p-8 rounded-lg w-96 m-8">
                <div className='flex justify-between items-center'>
                    <h1 className="text-2xl font-bold">Help</h1>
                    <Button icon={faX} onClick={() => setIsHelpModalVisible(false)} className="text-2xl font-bold bg-transparent" />
                </div>
                <p className="mt-4">For any queries, contact us at <a href="mailto:ccs@thapar.edu" className="text-blue-500 font-bold">ccs@thapar.edu</a>
                </p>
            </div>
        </div>
        <div className='select-none p-8 mb-8 rounded-xl shadow-lg text-white w-full h-16 bg-primary flex items-center justify-between'>
            <div className="flex-1 text-left font-bold text-2xl">
                <Link to="/">
                    Merch Store
                </Link>
            </div>
            <a draggable={false} href="https://ccstiet.com" target='_blank' className='relative w-[5.4rem] h-24 bg-primary rounded-[50%/40%] justify-center items-center mx-auto hidden sm:flex'>
                <img src={ccs_bulb} alt="Logo" className="p-2 select-none" draggable={false} />
            </a>
            <div className="relative sm:flex-1 flex justify-end">
                <FontAwesomeIcon icon={faBars} onClick={toggleDropdown} className="cursor-pointer font-bold text-2xl" />
                {isDropdownVisible && (
                    <div className="absolute right-0 top-12 w-48 bg-primary rounded-md shadow-lg z-10">
                        <ul>
                            {
                                authCtx.isLoggedIn && (
                                    <li
                                        className="px-4 py-2 hover:bg-primaryHover hover:rounded-md cursor-pointer"
                                        onClick={handleLogout}
                                    >
                                        Logout
                                    </li>
                                )
                            }
                            <li
                                className="px-4 py-2 hover:bg-primaryHover hover:rounded-md cursor-pointer"
                                onClick={handlePolicies}
                            >
                                Policies
                            </li>
                            <li
                                className="px-4 py-2 hover:bg-primaryHover hover:rounded-md cursor-pointer"
                                onClick={handleHelp}
                            >
                                Help
                            </li>
                        </ul>
                    </div>
                )}
            </div>
        </div>
    </>
    );
};

export default Navbar;
