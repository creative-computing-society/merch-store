import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../helpers/AxiosClient';
import { Carousel } from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css';
import { Button, Loader } from '../components';
import { faCartPlus } from '@fortawesome/free-solid-svg-icons';
import api_url from '../helpers/Config';

const Product = () => {
    const [loading, setLoading] = useState(true);
    const [product, setProduct] = useState({});
    const productId = useParams().id;
    const navigate = useNavigate();

    const [disabled, setDisabled] = useState(false);
    const [buttonText, setButtonText] = useState('Add to cart');

    const [name, setName] = useState('');
    const [size, setSize] = useState('');
    const [image, setImage] = useState(null);
    const [quantity, setQuantity] = useState(1);

    const [uploadedImageUrl, setUploadedImageUrl] = useState('');
    const [isUploading, setIsUploading] = useState(false); // New state variable

    const onImageSelect = (e) => {
        if (e.target.files[0].size > 15000000) {
            alert("File size should be below 15MB!");
            setImage(null);
        } else {
            setImage(e.target.files[0]);
        }
    };

    const uploadImage = async () => {
        const formData = new FormData();
        formData.append('file', image);
        formData.append('upload_preset', 'ccs-merch');
        formData.append('cloud_name', 'dgbobpgf4');

        try {
            setIsUploading(true); // Start uploading
            const response = await fetch('https://api.cloudinary.com/v1_1/dgbobpgf4/image/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            setUploadedImageUrl(data.url);
            setIsUploading(false); // End uploading
            return data.url;
        } catch (error) {
            setIsUploading(false); // End uploading on error
            throw new Error('Image upload failed');
        }
    };

    const addToCart = async () => {

        if (product.status !== 'allowed') {
            setDisabled(true);
            return;
        }

        if (product.is_name_required && !name) {
            alert('Name is required');
            return;
        }

        if (product.is_size_required && !size) {
            alert('Size is required');
            return;
        }

        if (product.is_image_required && !image) {
            alert('Image is required');
            return;
        }

        let imageUrl = uploadedImageUrl;
        if (product.is_image_required && !uploadedImageUrl) {
            try {
                imageUrl = await uploadImage();
            } catch (error) {
                alert('Image upload failed');
                return;
            }
        }

        try {
            const response = await api.post('/cart/add/', {
                product_id: productId,
                printing_name: product.is_name_required ? name : null,
                size: product.is_size_required ? size : null,
                image_url: product.is_image_required ? imageUrl : null,
                quantity: quantity
            });

            alert('Product added to cart');
            setButtonText('Already in cart');
            navigate('/');
        } catch (error) {
            if (error.response && error.response.status === 400) {
                alert('Product already in cart or quantity limit exceeded');
            }
        } finally {
            setDisabled(true);
        }
    };

    useEffect(() => {
        api.get(`/product/${productId}`)
            .then(response => {
                setLoading(false);
                setProduct(response);
                if (response.status !== 'allowed') {
                    if (response.status === 'incart') {
                        setDisabled(true);
                        setButtonText('Already in cart');
                    } else {
                        setDisabled(true);
                        setButtonText('Out of stock');
                    }
                }
            });
    }, [productId]);

    const handleQuantityChange = (event) => {
        const value = parseInt(event.target.value, 10);
        if (value > 0 && value <= product.max_quantity) {
            setQuantity(value);
        }
    };

    const increaseQuantity = () => {
        if (quantity < product.max_quantity) {
            setQuantity(quantity + 1);
        }
    };

    const decreaseQuantity = () => {
        if (quantity > 1) {
            setQuantity(quantity - 1);
        }
    };

    return (
        <div className={`flex flex-col md:flex-row gap-8 rounded-lg items-center w-full h-full ${isUploading ? "opacity-50 pointer-events-none" : "opacity-100 pointer-events-auto"} md:h-[calc(100vh-10rem)]`}>
            {isUploading && <div className='absolute w-full h-full flex justify-center items-center'>
                <Loader />
            </div>}
            <div className='flex flex-col rounded-lg p-8 shadow-lg border-2 h-full w-full md:w-1/3 bg-container justify-center items-center '>
                {loading ? <Loader /> :
                    <>
                        {
                            product.image2 ? <Carousel className='w-4/6' showThumbs={false} infiniteLoop={true} autoPlay={true} showStatus={false} showArrows={true}>
                                {product.image1 && <img src={`${api_url}${product.image1}`} alt='Product' className='object-contain' />}
                                {product.image2 && <img src={`${api_url}${product.image2}`} alt='Product' className='object-contain' />}
                            </Carousel> :
                                <Carousel className='w-4/6' showThumbs={false} infiniteLoop={true} autoPlay={true} showStatus={false} showArrows={true}>
                                    {product.image1 && <img src={`${api_url}${product.image1}`} alt='Product 22222' className='object-contain' />}
                                </Carousel>
                        }
                    </>

                }
            </div>
            <div className='rounded-lg p-4 shadow-lg border-2 h-full flex-1 bg-container w-full'>
                <div className='flex flex-col p-2 gap-8 h-full'>
                    {loading ? <Loader /> :
                        <>
                            <div>
                                <div className='text-3xl font-bold capitalize flex justify-between items-center'>
                                    {product.name}
                                    <div className='text-xl font-bold'>₹{product.price}</div>
                                </div>
                                <div className='text-l flex justify-between sm:items-center flex-col sm:flex-row'>
                                    {product.description}
                                    <div>Max Quantity: {product.max_quantity}</div>
                                </div>
                            </div>
                            <div className='flex flex-col gap-2'>
                                {product.is_name_required && (
                                    <div className='flex flex-col'>
                                        <label htmlFor='name' className='text-l'>Printing Name:</label>
                                        <input type='text' id='name' className='rounded-lg border-2 p-2' onChange={(e) => setName(e.target.value)} />
                                    </div>
                                )}
                                {product.is_size_required && (
                                    <div className='flex flex-col'>
                                        <label htmlFor='size' className='text-l'>Size:
                                            {product.size_chart_image && (
                                                <a href={product.size_chart_image} target='_blank' rel='noreferrer' className='ml-2 text-blue-500 text-xs'>
                                                    Size Chart
                                                </a>
                                            )}
                                        </label>
                                        <select id='size' className='rounded-lg border-2 p-2' value={size} onChange={(e) => setSize(e.target.value)}>
                                            <option>Select Size</option>
                                            <option value='S'>Small</option>
                                            <option value='M'>Medium</option>
                                            <option value='L'>Large</option>
                                            <option value='XL'>Extra Large</option>
                                        </select>
                                    </div>
                                )}
                                {product.is_image_required && (
                                    <div className='flex flex-col'>
                                        <label htmlFor='image' className='text-l'>Upload Image:</label>
                                        <input type='file' id='image' className='rounded-lg border-2 p-2' onChange={onImageSelect} />
                                    </div>
                                )}
                            </div>
                            <div className='mt-auto flex items-center gap-4'>
                                <div className='flex items-center gap-2'>
                                    <button onClick={decreaseQuantity} className='rounded-lg border-2 p-2'>-</button>
                                    <input type='number' value={quantity} onChange={handleQuantityChange} className='rounded-lg border-2 p-2 w-16 text-center' min='1' max={product.max_quantity} />
                                    <button onClick={increaseQuantity} className='rounded-lg border-2 p-2'>+</button>
                                </div>
                                <Button disabled={disabled || isUploading} text={buttonText} icon={faCartPlus} isActive className='w-full items-center flex justify-center py-2' onClick={addToCart} />
                            </div>
                        </>
                    }
                </div>
            </div>
        </div>
    );
};

export default Product;
