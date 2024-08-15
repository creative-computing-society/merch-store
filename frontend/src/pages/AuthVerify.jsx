import api from "../helpers/AxiosClient";
import React, { useContext, useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import AuthContext from "../helpers/AuthContext";
import { Loader } from "../components";

function AuthVerify() {
    const [searchParams, setSearchParams] = useSearchParams();
    const token = searchParams.get("token");
    const navigate = useNavigate();

    const [loading, setLoading] = useState(false);

    const authCtx = useContext(AuthContext);

    const verifyToken = async () => {
        setLoading(true);

        api.post("/auth/login/", { token: `${token}` }, false).then(response => {
            if (response.token) {
                authCtx.login(response);
                navigate("/");
            }
            setLoading(false);
        }).catch(error => {
            setLoading(false);
            navigate("/login");
        });
    };

    useEffect(() => {
        if (token) {
            verifyToken();
        }
        else {
            navigate("/login");
        }
    }, [token]);

    return (
        <div className="flex justify-center items-center">
            {loading && <Loader />}
        </div>
    );
}

export default AuthVerify;
