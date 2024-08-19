import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import Button from './Button';
import { faX, faDownload } from '@fortawesome/free-solid-svg-icons';

const QRPopup = ({ qrData }) => {
    confirmAlert({
        customUI: ({ onClose }) => {
            return (
                <div className={`flex items-center justify-center`}>
                    <div className="bg-white border p-8 rounded-lg w-96 m-8">
                        <div className='flex justify-between items-center'>
                            <h1 className="text-2xl font-bold">QR Code</h1>
                            <Button icon={faX} onClick={onClose} className="text-2xl font-bold bg-transparent" />
                        </div>
                        <img src={`data:image/png;base64,${qrData}`} className='w-full h-full' alt='QR Code' />
                        <p>Please take a screenshot or download the QR code for future reference.</p>
                        <Button className="px-4 py-2 mt-8 w-full" text="Download" icon={faDownload} onClick={() => {
                            const link = document.createElement('a');
                            link.href = `data:image/png;base64,${qrData}`;
                            link.download = 'qr_code.png';
                            link.click();
                        }} />
                    </div>
                </div>
            );
        }
    });
};

export default QRPopup;