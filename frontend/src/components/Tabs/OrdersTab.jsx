import { useEffect, useState } from 'react';
import api from '../../helpers/AxiosClient';
import Button from '../Button';
import { faDownload, faQrcode, faX } from '@fortawesome/free-solid-svg-icons';
import api_url from '../../helpers/Config';


export const OrdersTab = () => {
    const [orderedItems, setOrderedItems] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [orderIndex, setOrderIndex] = useState(0);
    useEffect(() => {
        fetchOrders();
    }, []);

    const fetchOrders = () => {
        api.get('/order/all/')
            .then(response => {
                setOrderedItems(response);
                console.log(response);
            });
    };
    return (
        <>
            <div className={`${isModalVisible ? "flex" : "hidden"} fixed z-50 inset-0 bg-black bg-opacity-50 items-center justify-center`}>
                <div className="bg-white p-8 rounded-lg w-96 m-8">
                    <div className='flex justify-between items-center'>
                        <h1 className="text-2xl font-bold">QR Code</h1>
                        <Button icon={faX} onClick={() => setIsModalVisible(false)} className="text-2xl font-bold bg-transparent" />
                    </div>
                    <img src={`data:image/png;base64,${orderedItems.length > 0 ? orderedItems[orderIndex].qr_code_data : ''
                        }`} className='w-full h-full' alt='QR Code' />
                    <p>Please take a screenshot or download the QR code for future reference.</p>
                    <Button className="px-4 py-2 mt-8 w-full" text="Download" icon={faDownload} onClick={() => {
                        const link = document.createElement('a');
                        link.href = `data:image/png;base64,${orderedItems.length > 0 ? orderedItems[orderIndex].qr_code_data : ''
                            }`;
                        link.download = 'qr_code.png';
                        link.click();
                    }} />
                </div>
            </div>
            <div className='flex flex-col h-full gap-4 justify-between'>
                <div className='flex overflow-auto flex-col flex-1 basis-0 gap-4'>
                    {orderedItems.length > 0 ? orderedItems.map((order, index) => (
                        <div key={index} className='flex flex-col gap-2 p-4 border-2 rounded-md'>
                            <div className='flex justify-between items-center'>
                                <div className='font-bold'>Order ID: {order.id}</div>
                                <div className='flex items-center gap-2'>
                                    <div className='text-xs'>{
                                        new Date(order.created_at).toLocaleString('en-US', {
                                            year: 'numeric',
                                            month: 'long',
                                            day: 'numeric',
                                            hour: 'numeric',
                                            minute: 'numeric',
                                            second: 'numeric'
                                        })
                                    }</div>
                                    <Button icon={faQrcode} isActive onClick={() => {
                                        setOrderIndex(index);
                                        setIsModalVisible(true);
                                    }} />
                                </div>
                            </div>
                            <div className='flex flex-col gap-2'>
                                {order.order_items.map((item, index) => (
                                    <div className='flex flex-col rounded-lg border-2 border-gray-200 bg-zinc-100'>
                                        <div key={index} className='flex justify-between items-center border-b-2 rounded-lg bg-white p-4'>
                                            {/* <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Placeholder_view_vector.svg/991px-Placeholder_view_vector.svg.png' alt={item.product.name} className='w-16 h-auto rounded-md' /> */}
                                            <img src={`${api_url}${item.product.image1}`} alt={item.product.name} className='w-1/3 h-auto rounded-md object-contain' />
                                            <div>{item.product.name}</div>
                                            <div>{item.quantity} x {item.product.price}</div>
                                        </div>
                                        <div className='p-2 rounded-b-lg text-xs'>
                                            <div>Printing Name: <span className='font-bold'>{item.printing_name}</span></div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))
                        : <div className='flex justify-center items-center h-full'>
                            <p>No previous orders to show!</p>
                        </div>
                    }
                </div>
            </div>
        </>
    );
};

export default OrdersTab;
