import React, { useEffect, useState } from 'react';
import api from '../helpers/AxiosClient';
import { useNavigate, useParams, Link } from 'react-router-dom';
import Button from '../components/Button';
import { faDownload, faHome, faQrcode } from '@fortawesome/free-solid-svg-icons';
import Loader from '../components/Loader';
import { faX } from '@fortawesome/free-solid-svg-icons';

const PaymentStatus = () => {
    const txnid = useParams().txnid;
    const [paymentDetails, setPaymentDetails] = useState({});
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    const [count, setCount] = useState(10);
    const [valid, setValid] = useState(false);
    const [isModalVisible, setIsModalVisible] = useState(false);

    useEffect(() => {
        api.post('/payment/verify/', { txnid: txnid })
            .then(response => {
                setPaymentDetails(response);
                if (response.status !== 'success') {
                    setValid(true);
                }
            }).catch(error => {
                setPaymentDetails({ error: error.message });
            }).finally(() => {
                setLoading(false);
            });
    }, [txnid]);

    useEffect(() => {
        if (!valid) return;
        if (count === 0) {
            navigate('/');
        }
        const timeout = setTimeout(() => {
            setCount(count - 1);
        }, 1000);
        return () => clearTimeout(timeout);
    }, [count, navigate, valid]);
    return (<>
        <div className={`${isModalVisible ? "flex" : "hidden"} fixed z-50 inset-0 bg-black bg-opacity-50 items-center justify-center`}>
            <div className="bg-white p-8 rounded-lg w-96 m-8">
                <div className='flex justify-between items-center'>
                    <h1 className="text-2xl font-bold">QR Code</h1>
                    <Button icon={faX} onClick={() => setIsModalVisible(false)} className="text-2xl font-bold bg-transparent" />
                </div>
                <img src={`data:image/png;base64,${paymentDetails.qr_code_data}`} className='w-full h-full' alt='QR Code' />
                <p>Please take a screenshot or download the QR code for future reference.</p>
                <Button className="px-4 py-2 mt-8 w-full" text="Download" icon={faDownload} onClick={() => {
                    const link = document.createElement('a');
                    link.href = `data:image/png;base64,${paymentDetails.qr_code_data}`;
                    link.download = 'qr_code.png';
                    link.click();
                }} />
            </div>
        </div>
        <div className='flex gap-8 rounded-lg items-center w-full md:h-[calc(100vh-10rem)] justify-center'>
            <div className='flex flex-col rounded-lg p-8 shadow-lg border-2 h-full w-full bg-container justify-center items-center md:p-16'>
                {!loading ?
                    !paymentDetails.error
                        ?
                        <>
                            <div className='text-center w-full m-auto'>
                                <p className='text-4xl font-bold text-center'>
                                    {paymentDetails.status === 'success' ? 'Payment Successful' : 'Payment Failed'}
                                </p>
                                {
                                    paymentDetails.status === 'success' ?
                                        <p className='text-green-500'>
                                            Your order has been placed successfully
                                        </p>
                                        :
                                        <p className='text-red-500'>
                                            Your order cannot be placed
                                        </p>
                                }
                            </div>
                            <hr className='my-6 border-2 rounded-lg w-1/2' />
                            <div className='flex flex-col gap-4 text-lg'>
                                <div>
                                    <span className='font-bold'>Transaction ID:</span> {paymentDetails.transaction_id}
                                </div>
                                <div>
                                    <span className='font-bold'>Payment Gateway ID:</span> {paymentDetails.payment_id}
                                </div>
                                <div>
                                    <span className='font-bold'>Paid Amount:</span> ₹{paymentDetails.paid_amount}
                                </div>
                                <div>
                                    <span className='font-bold'>Payment Status:</span> {paymentDetails.reason}
                                </div>
                                <div>
                                    <span className='font-bold'>Payment Date:</span> {
                                        new Date(paymentDetails.payment_date).toLocaleString('en-US', {
                                            year: 'numeric',
                                            month: 'long',
                                            day: 'numeric',
                                            hour: 'numeric',
                                            minute: 'numeric',
                                            second: 'numeric'
                                        })
                                    }
                                </div>
                            </div>
                            {!valid && <Button className="px-4 py-2 mt-8 w-full md:w-1/3" text="View QR Code" icon={faQrcode} isActive onClick={() => setIsModalVisible(true)} />}
                            <Link to="/" className='mt-4 w-full md:w-1/3 text-center'>
                                <Button className="px-4 py-2 w-full" text="Go to Home" icon={faHome} />
                            </Link>
                            {valid && <p className='mt-2 text-center m-auto'>or redirecting automatically in {count} {
                                count === 1 ? 'second' : 'seconds'
                            }</p>}
                        </>
                        :
                        <div className='w-full text-center'>
                            <p className='text-2xl font-bold text-center'>Invalid Transaction ID or Invalid Access</p>
                            <Link to="/">
                                <Button className="px-4 py-2 mt-8 w-full md:w-1/3" text="Go to Home" icon={faHome} isActive />
                            </Link>
                        </div>
                    :
                    <Loader />

                }
            </div>
        </div>
    </>
    );
};

export default PaymentStatus;