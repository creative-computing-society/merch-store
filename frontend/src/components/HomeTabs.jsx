import { useState, useContext } from 'react';
import { faCartShopping, faBagShopping, faUser } from '@fortawesome/free-solid-svg-icons';
import CartTab from './Tabs/CartTab';
import Button from './Button';
import AccountTab from './Tabs/AccountTab';
import OrdersTab from './Tabs/OrdersTab';
import AuthContext from '../helpers/AuthContext';
import { useNavigate } from 'react-router-dom';

const HomeTabs = () => {
    const navigate = useNavigate();
    const authCtx = useContext(AuthContext);
    const [activeTab, setActiveTab] = useState(0);
    const [loadedTabs, setLoadedTabs] = useState([0]); // Initialize with the first tab loaded

    const buttonComp = () => {
        return (
            <div className='w-full h-full justify-center items-center flex'>
                <Button
                    icon={faUser}
                    text="Login to view"
                    isActive
                    onClick={() => navigate('/login')}
                />
            </div>
        );
    };

    const tabs = [
        { id: 0, title: 'Cart', icon: faCartShopping, component: authCtx.isLoggedIn ? <CartTab /> : buttonComp() },
        { id: 1, title: 'Orders', icon: faBagShopping, component: authCtx.isLoggedIn ? <OrdersTab /> : buttonComp() },
        { id: 2, title: 'Account', icon: faUser, component: authCtx.isLoggedIn ? <AccountTab /> : buttonComp() },
    ];

    const handleTabClick = (index) => {
        setActiveTab(index);
        if (!loadedTabs.includes(index)) {
            setLoadedTabs([...loadedTabs, index]);
        }
    };

    return (
        <div className="flex flex-col h-full">
            <div className="flex justify-start items-center gap-2 py-4 overflow-x-auto">
                {tabs.map((tab, index) => (
                    <Button
                        key={index}
                        icon={tab.icon}
                        text={tab.title}
                        isActive={activeTab === index}
                        onClick={() => handleTabClick(index)}
                    />
                ))}
            </div>
            <div className="flex-1 mt-4">
                {tabs.map((tab, index) => (
                    <div
                        key={index}
                        className={`h-72 md:h-full transition-opacity duration-300 ${activeTab === index ? 'opacity-100' : 'opacity-0 hidden'}`}
                    >
                        {loadedTabs.includes(index) && tab.component}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default HomeTabs;
