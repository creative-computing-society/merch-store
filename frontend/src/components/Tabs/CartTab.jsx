import React, { useEffect, useState } from 'react';
import api from '../../helpers/AxiosClient';
import Button from '../Button';
import { faCartArrowDown, faMoneyBill } from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';
import api_url from '../../helpers/Config';
import confirmPopup from '../ConfirmPopup';

const CartTab = () => {
    const [cartProducts, setCartProducts] = useState([]);
    const [cartAmt, setCartAmt] = useState(0);
    const [isUpdating, setIsUpdating] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchCartItems();
    }, []);

    const fetchCartItems = () => {
        api.get('/cart/view/')
            .then(response => {
                setCartProducts(response.items);
                setCartAmt(response.total_amount);
            }).finally(() => {
                setLoading(false);
            });
    };

    const increaseQuantity = (productId) => {
        const updatedCart = cartProducts.map(product => {
            if (product.id === productId) {
                if (product.quantity < product.product.max_quantity) {
                    return { ...product, quantity: product.quantity + 1 };
                } else {
                    confirmPopup({
                        title: 'Max quantity reached',
                        message: `You can only add up to ${product.product.max_quantity} ${product.product.name} to your cart`,
                        isNoRequired: false,
                    });
                    return product;
                }
            }
            return product;
        });
        updateCart(updatedCart);
    };

    const decreaseQuantity = (productId, currentQuantity) => {
        if (currentQuantity === 1) {
            confirmPopup({
                title: 'Remove from cart',
                message: `Are you sure you want to remove ${cartProducts.find(product => product.id === productId)?.product.name} from your cart?`,
                onConfirm: () => {
                    setIsUpdating(true);
                    api.post('/cart/delete/', { cart_item_id: productId })
                        .then(() => {
                            fetchCartItems();
                        }).catch(error => {
                        }).finally(() => {
                            setIsUpdating(false);
                        });
                },
                onCancel: () => { }
            });
        } else {
            const updatedCart = cartProducts.map(product => {
                if (product.id === productId) {
                    return { ...product, quantity: product.quantity - 1 };
                }
                return product;
            });
            updateCart(updatedCart);
        }
    };

    const updateCart = (updatedCart) => {
        setIsUpdating(true);
        api.post('/cart/update/', { cart_items: updatedCart })
            .then((response) => {
                setCartProducts(response.items);
                setCartAmt(response.total_amount);
            }).finally(() => {
                setIsUpdating(false);
            });
    };

    return (!loading &&
        <div className='flex flex-col h-full gap-4 justify-between'>
            <div className={`${isUpdating ? 'opacity-50' : 'opacity-100'} transition duration-300 flex overflow-auto flex-col flex-1 basis-0 gap-4`}>
                {cartProducts.length > 0 ? cartProducts.map(product => (
                    <div key={product.id} className='rounded-lg border-2 border-gray-200 bg-zinc-100'>
                        <div className='flex justify-between items-center border-b-2 rounded-lg bg-white p-4'>
                            <img src={`${api_url}${product.product.image1}`} alt={product.product.name} className='w-1/3 h-auto rounded-md object-contain' />
                            <div>
                                <p>{product.product.name}</p>
                                <p className='font-bold'>INR {product.product.price}/-</p>
                            </div>
                            <div className='flex justify-center items-center'>
                                <div className='flex items-center'>
                                    {product.product.is_size_required ?
                                        <span>{product.size}</span>
                                        :
                                        <span>?</span>
                                    }
                                </div>
                                <div className='mx-4 h-8 border-l border-gray-600'></div>
                                {/* Quantity control */}
                                <div className='flex flex-col items-center'>
                                    <button className='rounded-lg py-1' onClick={() => increaseQuantity(product.id)} disabled={isUpdating}>+</button>
                                    <span>{product.quantity}</span>
                                    <button className='rounded-lg py-1' onClick={() => decreaseQuantity(product.id, product.quantity)} disabled={isUpdating}>-</button>
                                </div>
                            </div>
                        </div>
                        {product.product.is_name_required && (
                            <div className='p-2 rounded-b-lg text-xs'>
                                <div>Printing Name: <span className='font-bold'>{product.printing_name}</span></div>
                            </div>
                        )}
                    </div>
                )) :
                    <div className='flex justify-center items-center h-full'>
                        <p>Your cart is empty!</p>
                    </div>
                }
            </div>
            {cartProducts.length > 0 && <>
                <hr className='border-t-2 border-gray-200 rounded-lg' />
                <div>
                    <div className='flex flex-col'>
                        <div className='flex justify-between'>
                            <span>Subtotal:</span>
                            <span className='font-bold'>INR {cartAmt}/-</span>
                        </div>
                    </div>
                    <Link to='/checkout'>
                        <Button className='px-4 py-2 mt-4 w-full' disabled={isUpdating} icon={faCartArrowDown} isActive text="Checkout" />
                    </Link>
                </div>
            </>}

        </div>
    );
};

export default CartTab;
