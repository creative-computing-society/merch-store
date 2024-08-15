import { useState } from 'react';
import { faCartShopping, faBagShopping, faUser } from '@fortawesome/free-solid-svg-icons';
import CartTab from './Tabs/CartTab';
import Button from './Button';
import AccountTab from './Tabs/AccountTab';
import OrdersTab from './Tabs/OrdersTab';

const HomeTabs = () => {
    const [activeTab, setActiveTab] = useState(0);
    const [loadedTabs, setLoadedTabs] = useState([0]); // Initialize with the first tab loaded

    const tabs = [
        { id: 0, title: 'Cart', icon: faCartShopping, component: <CartTab /> },
        { id: 1, title: 'Orders', icon: faBagShopping, component: <OrdersTab /> },
        { id: 2, title: 'Account', icon: faUser, component: <AccountTab /> },
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
