import React, { useState } from 'react';

const Policies = () => {
    const [activePolicy, setActivePolicy] = useState(0);
    const policies = [
        {
            title: 'About Us',
            content: <><p>Welcome to the official merchandise store of the <b><u>Creative Computing Society (CCS)</u></b> at Thapar Institute of Engineering and Technology (TIET), Patiala. Our store is a dedicated platform where the vibrant student community of TIET can access a range of high-quality and exclusive merchandise that reflects the spirit and values of our esteemed society.</p>
                <br />
                <p>At the Creative Computing Society, we hold creativity, innovation, and community in the highest regard. Our collection is meticulously curated to embody these principles, offering products that go beyond mere clothing or accessories. Each item is crafted to serve as a proud symbol of our collective identity and unwavering commitment to the fields of computing and technology. Our designs are inspired by the dynamic culture of TIET and the innovative spirit of our society, ensuring that every product resonates deeply with our members and supporters.</p>
                <br />
                <p>This website represents more than just a shopping destination; it is a gateway to connecting with the essence of CCS. It is a reflection of our shared values and a testament to our dedication to excellence and creativity. Whether you are a current student, an alumnus, or an enthusiastic supporter of our mission, we believe our merchandise offers something that will resonate with you and enhance your connection to our community.</p>
                <br />
                <p>Our store is managed with great care and attention to detail to provide you with a seamless and enjoyable shopping experience. The website is operated and overseen by <b>Akarsh Srivastava</b>, the General Secretary of the Creative Computing Society. Akarsh, along with our dedicated team, is committed to upholding the highest standards of quality and service. We strive to ensure that every interaction with our store is smooth, pleasant, and meets your expectations.</p>
                <br />
                <p>Should you have any questions, feedback, or require support, please do not hesitate to reach out to us. We are here to assist you and ensure that your experience with us is both positive and fulfilling.</p>
                <br />
                <p>We extend our heartfelt thanks to you for supporting the Creative Computing Society and being an integral part of our journey. Together, we strive to push the boundaries of innovation and creativity. Your support helps us continue our mission and make a positive impact within our community.</p></>
        },
        {
            title: 'Contact Details',
            content: <> <p><b><u>Creative Computing Society</u></b><br />
                Thapar Institute of Engineering and Technology,<br />
                Patiala, Punjab, India - 147004</p>
                <br />
                <p>If you have any questions, concerns, or require assistance, please do not hesitate to reach out to us. We are here to help and ensure that your inquiries are addressed promptly.</p>

                <p><b><u>Contact Email:</u></b><br />
                    For all queries, please contact us at: <a href="mailto:ccs@thapar.edu"><b><u>ccs@thapar.edu</u></b></a></p>
                <br />
                <p>We value your feedback and look forward to assisting you with any questions or support you may need. Thank you for reaching out to the Creative Computing Society!</p></>
        },
        {
            title: 'Terms and Conditions',
            content: <><p>Welcome to the Creative Computing Society’s official merchandise store. By accessing and using our website, you agree to comply with and be bound by the following terms and conditions. Please read these terms carefully. If you do not agree with any part of these terms, you should not use our website.</p>

                <b><u>1. General Terms</u></b>
                <p>These terms and conditions govern your use of our website and the purchase of any merchandise from us. By using our website, you acknowledge that you have read, understood, and agree to be bound by these terms and conditions. We reserve the right to modify these terms at any time, and such changes will be effective immediately upon posting on the website. Your continued use of the website constitutes your acceptance of any changes to these terms.</p>

                <b><u>2. Use of the Website</u></b>
                <p>You agree to use the website only for lawful purposes and in a manner that does not infringe the rights of, restrict, or inhibit anyone else's use and enjoyment of the website. Prohibited behavior includes, but is not limited to, transmitting any material that is unlawful, threatening, defamatory, obscene, or otherwise objectionable.</p>

                <b><u>3. Intellectual Property</u></b>
                <p>The content, design, and layout of the website, including but not limited to text, graphics, images, logos, and trademarks, are the property of Creative Computing Society and are protected by intellectual property laws. You may not reproduce, distribute, or otherwise use any content from this website without our prior written consent.</p>

                <b><u>4. Product Information</u></b>
                <p>We strive to ensure that all product descriptions and specifications are accurate. However, we do not warrant that the descriptions or other content on our website are accurate, complete, reliable, current, or error-free. If a product offered by us is not as described, your sole remedy is to return it in unused condition.</p>

                <b><u>5. Ordering and Payment</u></b>
                <p>By placing an order, you agree to provide accurate and complete information. We reserve the right to refuse or cancel any order if we suspect fraudulent activity or other issues with the order. Payment must be made in full at the time of purchase. We accept various payment methods, which will be detailed during the checkout process.</p>

                <b><u>6. Limitation of Liability</u></b>
                <p>To the fullest extent permitted by law, Creative Computing Society shall not be liable for any indirect, incidental, special, or consequential damages arising out of or related to your use of the website or the purchase of any merchandise. Our liability is limited to the maximum extent permitted by law.</p>

                <b><u>7. Governing Law</u></b>
                <p>These terms and conditions are governed by and construed in accordance with the laws of TIET, without regard to its conflict of law principles. Any disputes arising from or related to these terms and conditions shall be subject to the exclusive jurisdiction of the courts located in Patiala.</p>

                <b><u>8. Contact Us</u></b>
                <p>If you have any questions about these terms and conditions or our shipping policy, please contact us at: <a href="mailto:ccs@thapar.edu"><b><u>ccs@thapar.edu</u></b></a></p>

                <p>Thank you for choosing to shop with us. We appreciate your support and look forward to serving you!</p></>
        },
        {
            title: 'Shipping Policy',
            content: <>
                <p><b><u>Shipping Method:</u></b><br />
                    We offer a convenient collection service for your orders. All products can be picked up from a designated area within the TIET campus. Once your order is confirmed, you will receive a QR code via email and in your order section on the website. This QR code will be required for collecting your items at the pickup location. Please ensure you have the QR code ready when you arrive.</p>

                <p><b><u>Shipping Charges:</u></b><br />
                    The price of your order includes all applicable shipping charges. There are no additional fees for delivery, as all costs are included in the total order amount.</p>

                <p><b><u>Order Tracking:</u></b><br />
                    Currently, we do not provide tracking information for orders. We appreciate your understanding and encourage you to contact us if you have any questions or concerns about your order.</p>

                <p><b><u>Lost or Damaged Shipments:</u></b><br />
                    If your order is lost or arrives damaged, please notify us immediately. We are committed to resolving such issues promptly. Depending on the situation, we may offer a replacement or a refund after investigating the matter. Your satisfaction is our priority, and we will work to address any concerns you may have.</p>
            </>

        },
        {
            title: 'Return and Cancellation Policy',
            content: <>
                <h2><b><u>No Cancellation Policy</u></b></h2>
                <p>Once an order has been placed and confirmed on our website, it cannot be canceled. We prioritize prompt processing and fulfillment of orders to ensure timely delivery. To avoid any inconvenience, we strongly advise you to review all order details, including product selection and shipping information, before finalizing your purchase. If you have any doubts or concerns, please address them before placing your order.</p>

                <h2><b><u>No Refund Policy</u></b></h2>
                <p>We do not offer refunds for any products purchased from the CCS Merch Store. Our no refund policy is in place because each item is custom-made to order. We are committed to maintaining the highest standards of quality and craftsmanship for all our products. Once an order is confirmed, we proceed with manufacturing and preparing your item specifically to your request, making it non-returnable and non-refundable.</p>
                <br />
                <p>We appreciate your understanding and cooperation regarding these policies. Our goal is to provide you with an exceptional shopping experience and high-quality merchandise. Should you have any questions or need further clarification, please do not hesitate to contact us.</p>
            </>

        },
        {
            title: 'Privacy Policy',
            content: <>
                <p>At Creative Computing Society (CCS), we value your privacy and are committed to protecting your personal information. This Privacy Policy outlines how we collect, use, and safeguard your data when you visit our website, make a purchase, or interact with us. By using our website, you consent to the practices described in this policy.</p>

                <h2><b><u>1. Information We Collect</u></b></h2>
                <p>When you engage with our website, whether by making a purchase, logging in, or contacting us, we may collect certain personal information from you. The types of information we collect include:</p>
                <ul>
                    <li>• <b>Your Name:</b> To personalize your experience and address you appropriately in communications.</li>
                    <li>• <b>Your Email Address:</b> To send order confirmations, updates, and respond to any inquiries you may have.</li>
                    <li>• <b>Your Phone Number:</b> For contacting you regarding order status, delivery updates, or any issues related to your order.</li>
                    <li>• <b>Your Position:</b> If relevant, to better understand your role and preferences related to our merchandise.</li>
                </ul>

                <h2><b><u>2. How We Use Your Information</u></b></h2>
                <p>The personal information we collect is used in several ways to ensure a smooth and efficient experience:</p>

                <h3><b>To Process and Fulfill Your Orders:</b></h3>
                <p>We use your information to manage and complete your orders. This includes:</p>
                <ul>
                    <li>• <b>Shipping Your Products:</b> To deliver the purchased merchandise to your specified address.</li>
                    <li>• <b>Sending Order Confirmation and Tracking Details:</b> To keep you informed about the status of your order and provide you with tracking information.</li>
                    <li>• <b>Managing Returns or Exchanges:</b> To handle any requests for returns or exchanges and process them in accordance with our policies.</li>
                </ul>

                <h3><b>To Communicate with You:</b></h3>
                <p>We may use your contact information to:</p>
                <ul>
                    <li>• <b>Send Updates About Your Order:</b> To notify you about any changes or updates related to your order.</li>
                    <li>• <b>Respond to Inquiries:</b> To answer any questions you may have and provide support regarding your purchases or our services.</li>
                    <li>• <b>Provide Customer Support:</b> To assist you with any issues or concerns you may encounter.</li>
                </ul>

                <h2><b><u>3. Data Security</u></b></h2>
                <p>We implement appropriate technical and organizational measures to protect your personal information from unauthorized access, disclosure, alteration, or destruction. Despite these measures, please be aware that no method of transmission over the internet or electronic storage is 100% secure, and we cannot guarantee absolute security.</p>

                <h2><b><u>4. Sharing Your Information</u></b></h2>
                <p>We do not sell, trade, or otherwise transfer your personal information to outside parties. However, we may share your information with third-party service providers who assist us in operating our website, conducting our business, or servicing you, provided that these parties agree to keep the information confidential and use it solely for the purposes specified.</p>

                <h2><b><u>5. Cookies and Tracking Technologies</u></b></h2>
                <p>Our website may use cookies and similar tracking technologies to enhance your browsing experience, analyze site traffic, and understand user behavior. Cookies are small files placed on your device that help us remember your preferences and improve our website's functionality. You can choose to disable cookies through your browser settings, but this may affect your experience on our site.</p>

                <h2><b><u>6. Your Rights</u></b></h2>
                <p>You have the right to access, correct, or delete your personal information. If you wish to exercise these rights or have any concerns about how we handle your data, please contact us using the information provided below.</p>

                <h2><b><u>7. Changes to This Privacy Policy</u></b></h2>
                <p>We may update this Privacy Policy from time to time to reflect changes in our practices or legal requirements. Any modifications will be posted on this page with an updated effective date. We encourage you to review this policy periodically to stay informed about how we are protecting your information.</p>

                <h2><b><u>8. Contact Us</u></b></h2>
                <p>If you have any questions, concerns, or requests regarding this Privacy Policy or how we handle your personal information, please contact us at: <a href="mailto:ccs@thapar.edu"><b><u>ccs@thapar.edu</u></b></a></p>
                <br />
                <p>Thank you for trusting Creative Computing Society with your personal information. We are committed to safeguarding your privacy and ensuring a secure and enjoyable experience on our website.</p>
            </>

        },
    ];
    return (
        <div className='flex flex-col md:flex-row gap-8 rounded-lg items-center w-full h-full'>
            <div className='flex flex-col rounded-lg p-6 shadow-lg border-2 h-full w-full md:w-1/3 bg-container'>
                <div className='text-3xl font-bold'>
                    Policies
                </div>
                <hr className='my-4 border-2 rounded-lg' />
                <div className='flex flex-col gap-2'>
                    {policies.map((policy, index) => (
                        <div
                            key={index}
                            className={`border-2 border-gray-200  p-2 rounded-md cursor-pointer ${activePolicy === index ? 'bg-primary text-white' : 'bg-zinc-100 text-primary hover:bg-primaryHover/5 hover:text-primary'}`}
                            onClick={() => setActivePolicy(index)}
                        >
                            {policy.title}
                        </div>
                    ))}
                </div>
            </div>
            <div id="prodCont" className='rounded-lg p-4 shadow-lg border-2 flex-1 bg-container overflow-auto md:h-[calc(100vh-10rem)] h-full'>
                <div className='h-full'>
                    <div className='p-2'>
                        <h1 className='text-2xl font-bold'>{policies[activePolicy].title}</h1>
                    </div>
                    <div className='p-2'>
                        {policies[activePolicy].content}
                    </div>

                </div>
            </div>
        </div>
    );
};

export default Policies;