import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import Button from './Button';
import { faX, faCheck, faMultiply } from '@fortawesome/free-solid-svg-icons';

const confirmPopup = ({ title, message, onConfirm, onCancel, isNoRequired = true }) => {
    confirmAlert({
        customUI: ({ onClose }) => {
            return (

                <div className={`flex items-center justify-center`}>
                    <div className="bg-white border p-8 rounded-lg w-96 m-8">
                        <div className='flex justify-between items-center'>
                            <h1 className="text-2xl font-bold">{title}</h1>
                            <Button icon={faX} onClick={onClose} className="text-2xl font-bold bg-transparent" />
                        </div>
                        <p className="mt-4">{message}</p>
                        <div className='flex items-center gap-2 mt-4'>
                            <Button icon={faCheck} text={
                                isNoRequired ? 'Yes' : 'OK'
                            } isActive onClick={() => {
                                onConfirm && onConfirm();
                                onClose();
                            }} className='' />
                            {isNoRequired && <Button icon={faMultiply} text="No" onClick={() => {
                                onCancel && onCancel();
                                onClose();
                            }} className='' />}
                        </div>
                    </div>
                </div>
            );
        }
    });
};

export default confirmPopup;