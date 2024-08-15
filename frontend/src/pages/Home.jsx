import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../helpers/AxiosClient';
import { HomeTabs, Loader } from '../components';
import api_url from '../helpers/Config';



const Home = ({ user }) => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get('/product/all')
            .then(response => {
                setProducts(response); // Assuming response.data contains the array of products
            }).finally(() => {
                setLoading(false);
            });
    }, []);

    return (
        <div className='flex flex-col md:flex-row gap-8 rounded-lg items-center w-full h-full'>
            <div className='flex flex-col rounded-lg p-6 shadow-lg border-2 h-full w-full md:w-1/3 bg-container'>
                <div className='text-3xl font-bold capitalize'>
                    Hello,
                    <br />
                    {user.name.split(' ')[0].toLowerCase()}!
                </div>
                <hr className='my-2 border-2 rounded-lg ' />
                <HomeTabs />
            </div>
            <div id="prodCont" className='rounded-lg p-4 shadow-lg border-2 flex-1 bg-container overflow-auto md:h-[calc(100vh-10rem)] w-full'>
                {loading ? <Loader /> : <div className='h-full'>
                    {products.length === 0 && <div className='flex justify-center items-center h-full'>
                        <p>No products to show!</p>
                    </div>}
                    <div className='grid md:grid-cols-3 gap-4 grid-cols-1 pb-4'>
                        {products.map(product => (
                            <Link to={`/product/${product.id}`} key={product.id} className='rounded-md p-4 border-2 bg-white flex flex-col hover:scale-105 transition-all'>
                                <div className="w-full h-80 overflow-hidden flex items-center justify-center">
                                    <img src={`${api_url}${product.image1}`} alt={product.name} className='w-full h-full object-contain border' />
                                </div>
                                <div className='text-xl mt-3'>{product.name}</div>
                                <div className='font-bold'>₹{product.price}/-</div>
                            </Link>
                        ))}
                    </div>
                </div>}
            </div>
        </div>
    );
};

export default Home;
