import { useEffect, useState } from 'react';
import api from '../../helpers/AxiosClient';
import Button from '../Button';
import { faDownload, faQrcode, faX } from '@fortawesome/free-solid-svg-icons';
import api_url from '../../helpers/Config';
import QRPopup from '../QRPopup';


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
                                        QRPopup({ qrData: order.qr_code_data });
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
                                            <div className='font-bold'>{item.quantity} x INR {item.product.price}/-</div>
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
