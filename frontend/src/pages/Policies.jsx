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
            content: <>
                <p>You may contact us using the information below:</p>
                <br />
                <p><b>Merchant Legal Entity Name:</b> AKARSH SRIVASTAVA</p>
                <p><b>Registered Address:</b> Thapar Institute of Engineering and Technology, Patiala, Punjab, PIN: 147004</p>
                <p><b>Operational Address:</b> Thapar Institute of Engineering and Technology, Patiala, Punjab, PIN: 147004</p>
                <p><b>Telephone No:</b> 8920455673</p>
                <p><b>E-Mail ID:</b> <a href="mailto:pagarwal_be22@thapar.edu">pagarwal_be22@thapar.edu</a></p>
            </>
        },
        {
            title: 'Terms and Conditions',
            content: (
                <>
                    <p>These Terms and Conditions, along with privacy policy or other terms (“Terms”) constitute a binding agreement by and between AKARSH SRIVASTAVA, ( “Website Owner” or “we” or “us” or “our”) and you (“you” or “your”) and relate to your use of our website, goods (as applicable) or services (as applicable) (collectively, “Services”).</p>

                    <p>By using our website and availing the Services, you agree that you have read and accepted these Terms (including the Privacy Policy). We reserve the right to modify these Terms at any time and without assigning any reason. It is your responsibility to periodically review these Terms to stay informed of updates.</p>

                    <p>The use of this website or availing of our Services is subject to the following terms of use:</p>

                    <b><u>1. Information Accuracy</u></b>
                    <p>To access and use the Services, you agree to provide true, accurate and complete information to us during and after registration, and you shall be responsible for all acts done through the use of your registered account.</p>

                    <b><u>2. Warranty Disclaimer</u></b>
                    <p>Neither we nor any third parties provide any warranty or guarantee as to the accuracy, timeliness, performance, completeness or suitability of the information and materials offered on this website or through the Services, for any specific purpose. You acknowledge that such information and materials may contain inaccuracies or errors and we expressly exclude liability for any such inaccuracies or errors to the fullest extent permitted by law.</p>

                    <b><u>3. User Responsibility</u></b>
                    <p>Your use of our Services and the website is solely at your own risk and discretion. You are required to independently assess and ensure that the Services meet your requirements.</p>

                    <b><u>4. Intellectual Property</u></b>
                    <p>The contents of the Website and the Services are proprietary to Us and you will not have any authority to claim any intellectual property rights, title, or interest in its contents.</p>

                    <b><u>5. Unauthorized Use</u></b>
                    <p>You acknowledge that unauthorized use of the Website or the Services may lead to action against you as per these Terms or applicable laws.</p>

                    <b><u>6. Payment of Services</u></b>
                    <p>You agree to pay us the charges associated with availing the Services.</p>

                    <b><u>7. Prohibited Usage</u></b>
                    <p>You agree not to use the website and/or Services for any purpose that is unlawful, illegal, or forbidden by these Terms, or Indian or local laws that might apply to you.</p>

                    <b><u>8. Third-Party Links</u></b>
                    <p>You agree and acknowledge that the website and the Services may contain links to other third-party websites. On accessing these links, you will be governed by the terms of use, privacy policy, and such other policies of such third-party websites.</p>

                    <b><u>9. Legal Binding</u></b>
                    <p>You understand that upon initiating a transaction for availing the Services you are entering into a legally binding and enforceable contract with us for the Services.</p>

                    <b><u>10. Refund Policy</u></b>
                    <p>You shall be entitled to claim a refund of the payment made by you in case we are not able to provide the Service. The timelines for such return and refund will be according to the specific Service you have availed or within the time period provided in our policies (as applicable). In case you do not raise a refund claim within the stipulated time, then this would make you ineligible for a refund.</p>

                    <b><u>11. Force Majeure</u></b>
                    <p>Notwithstanding anything contained in these Terms, the parties shall not be liable for any failure to perform an obligation under these Terms if performance is prevented or delayed by a force majeure event.</p>

                    <b><u>12. Governing Law</u></b>
                    <p>These Terms and any dispute or claim relating to it, or its enforceability, shall be governed by and construed in accordance with the laws of India.</p>

                    <b><u>13. Jurisdiction</u></b>
                    <p>All disputes arising out of or in connection with these Terms shall be subject to the exclusive jurisdiction of the courts in Patiala, Punjab.</p>

                    <b><u>14. Contact Information</u></b>
                    <p>All concerns or communications relating to these Terms must be communicated to us using the contact information provided on this website.</p>
                </>
            )
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